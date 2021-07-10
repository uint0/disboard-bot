import asyncio

import fastapi

import bot
import config

from .routes import event_handlers

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.bot.start(config.discord.DISCORD_BOT_TOKEN))


@app.get('/healthcheck')
async def healthcheck():
    return {"status": "up"}


app.include_router(event_handlers.events_router, prefix="/events")
