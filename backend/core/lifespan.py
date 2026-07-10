import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from supabase import create_async_client
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from database.postgre.engine import engine, Base
from api.routes.slack import slack_app


from core.config import Settings


SUPABASE_URL = Settings.SUPABASE_URL
SUPABASE_KEY = Settings.SUPABASE_KEY
app_token = Settings.SLACK_APP_TOKEN


@asynccontextmanager
async def lifespan(app: FastAPI):
    socket_handler = AsyncSocketModeHandler(app=slack_app, app_token=app_token)

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    except Exception as e:
        print(f"Warning: Failed to initialize database: {e}")

    app.state.supabase = await create_async_client(SUPABASE_URL, SUPABASE_KEY)

    slack_task = asyncio.create_task(socket_handler.start_async())

    yield

    await engine.dispose()

    await socket_handler.close_async()
    slack_task.cancel()
