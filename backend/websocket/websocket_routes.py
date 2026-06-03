import asyncio

from fastapi import APIRouter, WebSocket

from events.event_manager import event_manager


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await event_manager.connect(websocket)

    try:
        while True:
            # await websocket.receive_text()
            await asyncio.sleep(1)

    except Exception:
        event_manager.disconnect(websocket)