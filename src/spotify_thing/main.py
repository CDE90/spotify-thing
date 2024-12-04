import asyncio

import sqlalchemy
import sqlalchemy.ext.asyncio

from db import models, query
from spotify_thing import config

POSTGRES_URI = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"


async def main():
    # Connect to the database
    engine = sqlalchemy.ext.asyncio.create_async_engine(POSTGRES_URI)

    async with engine.connect() as conn:
        # Create a querier
        querier = query.AsyncQuerier(conn)

        # Get all authors
        authors = [author async for author in querier.list_authors()]
        print(authors)

        # Add a new author
        await querier.create_author(name="John Doe", bio="I am a test author")

        # Get all authors again
        authors = [author async for author in querier.list_authors()]
        print(authors)

        # Commit the changes
        await conn.commit()


if __name__ == "__main__":
    asyncio.run(main())
