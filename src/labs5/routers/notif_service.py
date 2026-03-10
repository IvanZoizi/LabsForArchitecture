from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

send_router = APIRouter()

class MessageModel(BaseModel):
    text: str

class ObjectModel(BaseModel):
    obj: dict[str, Any]

@send_router.post("/send/message")
async def sendMessage(request: Request, model: MessageModel):
    rabbitMQ = request.app.state.rabbitMQ
    await rabbitMQ.send_message(model.text)
    return JSONResponse({"error": False})


@send_router.post('/send/obj')
async def sendObj(request: Request, model: ObjectModel):
    rabbitMQ = request.app.state.rabbitMQ
    await rabbitMQ.send_obj(model.obj)
    return JSONResponse({"error": False})


@send_router.get('/last/message')
async def lastMessage(request: Request):
    rabbitMQ = request.app.state.rabbitMQ
    return JSONResponse({"message": await rabbitMQ.get_message()})