from typing import Annotated

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, HTTPException, Request, Depends, Form, File, UploadFile, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.labs4.utils.dbase import Dbase, get_db

clientRouter = APIRouter()


@clientRouter.get('/get/client')
async def getClient(dbase: Annotated[Dbase, Depends(get_db)],
                    clientId: int = Query(...)):
    client = dbase.getClient(clientId)
    if not client:
        return JSONResponse({"success": False, "error": "This client is not find"})
    return JSONResponse({"success": True,
                          "clientId": client[0],
                          "clientName": client[1],
                          "clientSurname": client[2]})


@clientRouter.post('/new/client')
async def newClient(dbase: Annotated[Dbase, Depends(get_db)],
                    clientName: str = Form(...),
                    clientSurName: str = Form(...)):
    clientId = dbase.newClient(clientName, clientSurName)
    if clientId < 0:
        return JSONResponse({"success": False, "error": "This day and time is busy"})
    return JSONResponse({"success": True, "clientID ": clientId})

