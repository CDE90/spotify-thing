import asyncio
import re

import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlparse  # type: ignore[import-untyped]

from spotify_thing import config

POSTGRES_URI = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"


async def main():
    # Connect to the database
    engine = sqlalchemy.ext.asyncio.create_async_engine(POSTGRES_URI)

    async with engine.connect() as conn:
        # Check that that user wants to drop the tables
        res = input("Are you sure you want to drop the tables? [y/N] ")
        if res.lower() != "y":
            print("Aborting")
            return

        # Read the schema.sql file
        with open("src/db/schema.sql", "r") as fd:
            schema = fd.read()

        # Get the table names
        table_names = re.findall(r"CREATE TABLE (\w+)", schema)

        # Drop all tables
        for table_name in table_names:
            res = await conn.execute(
                sqlalchemy.text(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            )
            print(res)

        print("Tables dropped")

        # Create the tables
        statements = sqlparse.split(schema)

        for statement in statements:
            if statement.strip() == "":
                continue

            res = await conn.execute(sqlalchemy.text(statement))
            print(res)

        print("Tables created")

        # Commit the changes
        await conn.commit()


if __name__ == "__main__":
    asyncio.run(main())
