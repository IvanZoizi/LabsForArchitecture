from typing import Annotated

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, HTTPException, Request, Depends, Form, File, UploadFile, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.labs4.utils.dbase import Dbase, get_db

appointmentRouter = APIRouter()

@appointmentRouter.post('/create/appointment')
async def create_appointment(dbase: Annotated[Dbase, Depends(get_db)],
                             clientId: int = Form(...),
                             date: str = Form(...),
                             time: str = Form(...),
                             ):
    client = dbase.getClient(clientId)
    if not client:
        return JSONResponse({"success": False, "error": "Client is not find"})
    idAppointment = dbase.createNewAppointment(clientId, date, time)
    if idAppointment < 0:
        return JSONResponse({"success": False, "error": "This day and time is busy"})
    return JSONResponse({"success": True, "idAppointment": idAppointment})

@appointmentRouter.get('/get/appointment')
async def appointment(dbase: Annotated[Dbase, Depends(get_db)], idAppointment: int = Query(...)):
    appointment = dbase.getAppointment(idAppointment)
    if appointment:
        return JSONResponse({"success": True, "idAppointment": idAppointment, "idClient": appointment[1],
                             "date": appointment[2], "time": appointment[3], 'status': appointment[4]})
    return JSONResponse({"success": False, "error": "This idAppointment is not find"})


@appointmentRouter.get('/get/appointments')
async def appointments(dbase: Annotated[Dbase, Depends(get_db)]):
    appointments = dbase.getAppointments()
    resultList = []
    for appointment in appointments:
        resultList.append({
            "idAppointment": appointment[0],
            "idClient": appointment[1],
            "date": appointment[2],
            "time": appointment[3],
            'status': appointment[4]
        })
    return JSONResponse({"appointments": resultList})


@appointmentRouter.post('/accept/appointment')
async def appointment(dbase: Annotated[Dbase, Depends(get_db)],
                      idAppointment: int = Form(...)):
    appointment = dbase.getAppointment(idAppointment)
    if not appointment:
        return JSONResponse({"success": False, "error": "This appintment is not find"})
    dbase.update_status(idAppointment, "Confirmed")
    return JSONResponse({"success": True, "idAppointment": idAppointment})


@appointmentRouter.post('/close/appointment')
async def close(dbase: Annotated[Dbase, Depends(get_db)],
                      idAppointment: int = Form(...)):

    appointment = dbase.getAppointment(idAppointment)
    if not appointment:
        return JSONResponse({"success": False, "error": "This appintment is not find"})
    dbase.update_status(idAppointment, "Finished")
    return JSONResponse({"success": True, "idAppointment": idAppointment})