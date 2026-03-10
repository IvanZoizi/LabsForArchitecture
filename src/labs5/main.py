import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import dotenv

from routers import list_routers
from utils import rabbitmq

dotenv.load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitMQ = rabbitmq.RabbitMQ(os.getenv("URL_FOR_RABBIT"))
    await rabbitMQ.connect()
    await rabbitMQ.clear_queue()
    app.state.rabbitMQ = rabbitMQ
    yield
    await rabbitMQ.close()

app = FastAPI(title="Labs 5", version="1.0.0", lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    for router in list_routers:
        app.include_router(router)
    uvicorn.run(app, host="127.0.0.1", port=8000)