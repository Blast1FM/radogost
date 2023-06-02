import websockets
import asyncio

class VideoServer():
    def __init__(self):
        self.host = "localhost"
        self.port = 7473
    
    async def convert_frame_to_bytes(self,frame):
        return bytes(frame)

    async def producer_handler(self, websocket):
        while True:
            message = await self.convert_frame_to_bytes()
            await websocket.send(message)

    async def main(self):
        srv = await asyncio.start_server(
            self.producer_handler(srv), self.host, self.port)
        await srv.serve_forever()
    
    #TODO implement in detection.py