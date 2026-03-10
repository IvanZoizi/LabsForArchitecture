from .appointments import appointmentRouter
from .clients import clientRouter


routersList = [
    appointmentRouter,
    clientRouter
]