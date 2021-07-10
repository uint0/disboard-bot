import typing

import fastapi

from ..models import events
from ..security import hmac

import bot
import config

class AuthedEventRoute(fastapi.routing.APIRoute):
    def get_route_handler(self) -> typing.Callable:
        original_route_handler = super().get_route_handler()

        async def custom_handler(request: fastapi.Request) -> fastapi.Response:
            body = await request.body()
            sent_hmac = request.headers.get("X-Event-Payload-HMAC", "")
            if not hmac.ensure_request_integrity(body, sent_hmac):
                return fastapi.Response(status_code=403)

            return await original_route_handler(request)
        
        return custom_handler


events_router = fastapi.APIRouter(route_class=AuthedEventRoute)


@events_router.post("/minecraft/player_connection", tags=["events"])
async def minecraft_player_connect(
    connection_event: events.minecraft.MinecraftPlayerConnectionEvent
):
    await bot.bot.get_cog('MinecraftCommand').player_connection(
        connection_type=connection_event.connection_event_type.value,
        player_name=connection_event.player_name,
        server_name=connection_event.server_info.name,
        server_type=connection_event.server_info.type.value
    )
    return "ok"
