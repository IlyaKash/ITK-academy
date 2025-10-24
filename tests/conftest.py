import pytest
import pytest_asyncio
import asyncio
import sys
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="function")
def event_loop():
    """Create a new event loop for each test function."""
    if sys.platform == "win32":
        loop = asyncio.SelectorEventLoop()
    else:
        loop = asyncio.new_event_loop()
    
    asyncio.set_event_loop(loop)
    yield loop
    
    try:
        loop.run_until_complete(asyncio.sleep(0.1))
    except:
        pass
    finally:
        loop.close()

@pytest_asyncio.fixture(scope="function")
async def client():
    """Create a new client for each test"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client