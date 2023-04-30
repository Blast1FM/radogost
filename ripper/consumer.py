import asyncio
import websockets
import ssl

class Consumer():

    def __init__(self):
        self.bin_data:str
        self.uri:str
        self.token:str

    def set_credentials(self,uri,token):
        self.uri = uri
        self.token = token

    async def consume(self, data):
        print(data)

    async def consume_handler(self, websocket):
        async for message in websocket:
            await self.consume(message)

    def get_bin_data(self):
        return self.bin_data

async def main():
    client = Consumer()
    context = ssl.create_default_context()
    client.set_credentials("wss://msk204.extcam.com/ws-fmp4/live?server=100-EPywIFWmgDpEPV0tTLcUf8&camera=0&access_token=public&streams=video&vcodec=h264&acodec=aac&acodec=mp3&acodec=pcma&acodec=pcmu&acodec=none&duration=0&q=2&d=msk204.extcam.com&public=1&owner_id=100002041948&u=100002683733&ts=1682854043.6779943&token=c0e3f32a64c24e7ed98271959485eac6", "lpJlNFNG4GGPGkWtA0ZacVbi2GE=")
    async with websockets.connect(client.uri) as socket:
        await client.consume_handler(socket)

asyncio.run(main())