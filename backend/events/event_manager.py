import asyncio

class EventManager:
    def __init__(self) -> None:
        self.connections = []

    async def connect(self, websocket): 
        await websocket.accept() 
        self.connections.append(websocket)
    
    def disconnect(self, websocket):
        self.connections.remove(websocket)
    
    async def broadcast(self, message: dict):

        disconnected = []
        # print("Broadcasting",message)
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        for d in disconnected:
            self.disconnect(d)

event_manager = EventManager()