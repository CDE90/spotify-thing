from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class LenientBaseModel(BaseModel):
    """
    Base model that allows extra fields and ignores them during validation
    """

    model_config = ConfigDict(
        extra="ignore",  # Ignore any extra fields
        populate_by_name=True,  # Allow population by field names
        arbitrary_types_allowed=True,  # Allow arbitrary types
    )


class ExternalUrlObject(LenientBaseModel):
    pass


class ExternalIdObject(LenientBaseModel):
    pass


class ImageType(LenientBaseModel):
    height: Optional[int] = None
    width: Optional[int] = None
    url: str


class SimplifiedArtistObject(LenientBaseModel):
    external_urls: dict[str, str]
    href: str
    id: str
    name: str
    type: Literal["artist"] = "artist"
    uri: str


class SimplifiedAlbumObject(LenientBaseModel):
    album_type: Literal["album", "single", "compilation"]
    total_tracks: int
    available_markets: list[str]
    external_urls: dict[str, str]
    href: str
    id: str
    images: list[ImageType]
    name: str
    release_date: str
    release_date_precision: str
    type: Literal["album"] = "album"
    uri: str
    artists: list[SimplifiedArtistObject]
    # Any additional fields will be silently ignored


class TrackObject(LenientBaseModel):
    album: Optional[SimplifiedAlbumObject] = None
    artists: list[SimplifiedArtistObject]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: Optional[ExternalIdObject] = None
    external_urls: Optional[dict[str, str]] = None
    href: str
    id: str
    is_playable: bool = True
    name: str
    popularity: int
    preview_url: Optional[str] = None
    track_number: int
    type: Literal["track"] = "track"
    uri: str
    is_local: bool
    # Any additional fields will be silently ignored


class DeviceType(LenientBaseModel):
    id: Optional[str] = None
    is_active: bool = False
    is_private_session: bool = False
    is_restricted: bool = False
    name: str = ""
    type: str = ""
    volume_percent: Optional[int] = None
    supports_volume: bool = False


class ContextType(LenientBaseModel):
    type: str
    href: str
    external_urls: dict[str, str]
    uri: str


class TokenResponse(LenientBaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str


class DisallowsObject(LenientBaseModel):
    # Allows any additional keys beyond these
    resuming: Optional[bool] = None
    toggling_repeat_context: Optional[bool] = None
    toggling_repeat_track: Optional[bool] = None
    toggling_shuffle: Optional[bool] = None


class NowPlayingResponse(LenientBaseModel):
    device: DeviceType = Field(default_factory=DeviceType)
    repeat_state: Literal["off", "track", "context"] = "off"
    shuffle_state: bool = False
    context: Optional[ContextType] = None
    timestamp: int
    progress_ms: int
    is_playing: bool
    item: Optional[TrackObject] = None
    currently_playing_type: str
    actions: dict[str, Any] = Field(default_factory=dict)
