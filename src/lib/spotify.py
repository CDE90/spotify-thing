import asyncio
import base64

import aiohttp

from lib.spotify_types import NowPlayingResponse, TokenResponse
from spotify_thing import config

BASIC_AUTH = base64.b64encode(
    f"{config.SPOTIFY_CLIENT_ID}:{config.SPOTIFY_CLIENT_SECRET}".encode("utf-8")
).decode("utf-8")
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
NOW_PLAYING_ENDPOINT = "https://api.spotify.com/v1/me/player/currently-playing"


class SpotifyClient:
    def __init__(self):
        self._token = None

    async def _get_token(self) -> TokenResponse:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                TOKEN_ENDPOINT,
                headers={
                    "Authorization": f"Basic {BASIC_AUTH}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": config.SPOTIFY_REFRESH_TOKEN,
                },
            )

            if response.status != 200:
                raise Exception(f"Failed to get token: {response.status}")

            data = await response.json()

            return TokenResponse(**data)

    async def get_token(self, force_refresh: bool = False) -> TokenResponse:
        if self._token is None or force_refresh:
            self._token = await self._get_token()

        return self._token

    async def get_now_playing(self, retry: bool = True) -> NowPlayingResponse:
        token = await self.get_token()

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                NOW_PLAYING_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {token.access_token}",
                },
            )

            if retry and response.status == 401:
                token = await self.get_token(force_refresh=True)
                return await self.get_now_playing(retry=False)

            if response.status != 200:
                raise Exception(f"Failed to get now playing: {response.status}")

            data = await response.json()

            return NowPlayingResponse(**data)


async def main():
    client = SpotifyClient()
    token = await client.get_token()

    print(token)
    print(token.access_token)

    now_playing = await client.get_now_playing()

    if now_playing.is_playing:
        # Get the currently playing track
        track = now_playing.item
        print(f"Currently playing: '{track.name}' - {track.artists[0].name}")

    else:
        print("Not playing")


if __name__ == "__main__":
    asyncio.run(main())
