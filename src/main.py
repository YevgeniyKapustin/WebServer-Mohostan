from fastapi import FastAPI

from commands.controller import router as commands_router

app = FastAPI()


app.include_router(commands_router)
