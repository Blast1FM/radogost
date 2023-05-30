import websockets
import asyncio

class VideoServer():
    def __init__(self):
        self.host = "localhost"
        self.port = 7473
    
    async def send_frame(self,frame):
        #convert to bytes first lmao eejit
        return frame

    async def producer_handler(self, websocket):
        while True:
            message = await self.send_frame()
            await websocket.send(message)

    #oi blyat implement this 