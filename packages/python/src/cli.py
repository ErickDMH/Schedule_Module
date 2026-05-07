import argparse
import asyncio
import os
import re
import asyncpg
from src.db.connection import DATABASE_URL

ASYNC_PG_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
DB_DIR = os.path.join(PROJECT_ROOT, "db")

async def run_sql_file(conn, filepath):
    with open(filepath, "r") as f:
        sql = f.read()
    if sql.strip():
        await conn.execute(sql)

async def init_schema_version(conn):
    # Ensure the table exists
    await conn.execute("""
        CREATE SCHEMA IF NOT EXISTS schedule_module;
        CREATE TABLE IF NOT EXISTS schedule_module.schema_version (
            version INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)

async def get_applied_migrations(conn):
    rows = await conn.fetch("SELECT version FROM schedule_module.schema_version")
    return {row['version'] for row in rows}

async def apply_migrations(conn):
    await init_schema_version(conn)
    applied = await get_applied_migrations(conn)

    migrations_dir = os.path.join(DB_DIR, "migrations")
    files = sorted(os.listdir(migrations_dir))
    
    for filename in files:
        if not filename.endswith(".sql"):
            continue
        
        match = re.match(r"^(\d+)_", filename)
        if match:
            version = int(match.group(1))
            if version not in applied:
                print(f"Applying migration: {filename}")
                filepath = os.path.join(migrations_dir, filename)
                await run_sql_file(conn, filepath)
                await conn.execute(
                    "INSERT INTO schedule_module.schema_version (version, name) VALUES ($1, $2)",
                    version, filename
                )
        else:
            print(f"Skipping incorrectly formatted migration file: {filename}")

async def bootstrap():
    print("Running bootstrap...")
    conn = await asyncpg.connect(ASYNC_PG_URL)
    try:
        # Run DDLs
        ddl_dir = os.path.join(DB_DIR, "ddl")
        for filename in sorted(os.listdir(ddl_dir)):
            if filename.endswith(".sql") and filename != "schema.sql":
                print(f"Applying DDL: {filename}")
                await run_sql_file(conn, os.path.join(ddl_dir, filename))
        
        # Apply Migrations
        await apply_migrations(conn)
    finally:
        await conn.close()
    print("Bootstrap complete.")

async def seed():
    print("Running seed...")
    conn = await asyncpg.connect(ASYNC_PG_URL)
    try:
        seed_path = os.path.join(DB_DIR, "bootstrap", "seed.sql")
        if os.path.exists(seed_path):
            await run_sql_file(conn, seed_path)
            print("Seed complete.")
        else:
            print("No seed.sql found.")
    finally:
        await conn.close()

def main():
    parser = argparse.ArgumentParser(description="Schedule Module CLI")
    parser.add_argument("command", choices=["bootstrap", "migrate", "seed"], help="Command to execute")

    args = parser.parse_args()

    if args.command == "bootstrap":
        asyncio.run(bootstrap())
    elif args.command == "migrate":
        async def _migrate():
            conn = await asyncpg.connect(ASYNC_PG_URL)
            try:
                await apply_migrations(conn)
            finally:
                await conn.close()
        asyncio.run(_migrate())
    elif args.command == "seed":
        asyncio.run(seed())

if __name__ == "__main__":
    main()
