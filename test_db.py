"""
Database connection test script.
Tests connectivity to PostgreSQL and verifies the setup.
"""
import asyncio
import sys
from sqlalchemy import text
from app.core.database import engine
from app.core.config import settings


async def test_db_connection():
    """Test database connection."""
    print("=" * 60)
    print("OpenClaw Backend - Database Connection Test")
    print("=" * 60)
    print(f"\nEnvironment: {settings.APP_ENV}")
    print(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print("\n" + "-" * 60)

    try:
        print("\n1. Testing database connection...")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"   ✓ Connection successful!")
            print(f"   ✓ PostgreSQL version: {version.split(',')[0]}")

        print("\n2. Testing query execution...")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1 + 1 as result"))
            test_result = result.scalar()
            print(f"   ✓ Query execution successful! (1 + 1 = {test_result})")

        print("\n3. Checking database name...")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT current_database()"))
            db_name = result.scalar()
            print(f"   ✓ Connected to database: {db_name}")

        print("\n4. Checking existing tables...")
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = result.fetchall()
            if tables:
                print(f"   ✓ Found {len(tables)} table(s):")
                for table in tables:
                    print(f"     - {table[0]}")
            else:
                print("   ⚠ No tables found (database needs initialization)")

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\n" + "=" * 60)
        print("✗ TESTS FAILED!")
        print("=" * 60)
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    success = asyncio.run(test_db_connection())
    sys.exit(0 if success else 1)

