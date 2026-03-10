import asyncio
import json
import os
import aio_pika

class RabbitMQ:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.queue_name = "MyQueue"
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            self.queue = await self.channel.declare_queue(
                self.queue_name,
                durable=False,
                auto_delete=False
            )

    async def send_message(self, message):
        if self.channel is None or self.connection is None:
            await self.connect()

        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode('utf-8')),
            routing_key=self.queue_name
        )

    async def send_obj(self, obj):
        json_data = json.dumps(obj)
        await self.send_message(json_data)

    async def clear_queue(self):
        count = 0
        while True:
            try:
                message = await self.queue.get(timeout=1, fail=False)
                if message:
                    async with message.process():
                        count += 1
                else:
                    break
            except asyncio.TimeoutError:
                break
            except aio_pika.exceptions.QueueEmpty:
                return

    async def get_message(self):
        message = await self.queue.get(timeout=5, fail=False)
        if message:
            async with message.process():
                return message.body.decode()
        return None

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()


async def main():
    import dotenv
    dotenv.load_dotenv('..')
    r = RabbitMQ(os.getenv("URL_FOR_RABBIT"))

    await r.connect()
    await r.clear_queue()

    await r.send_message("Hello")
    await r.send_message(" ")
    await r.send_message("World")

    while True:
        mes = await r.get_message()
        if not mes:
            break
        print(mes, end='')


if __name__ == '__main__':
    asyncio.run(main())