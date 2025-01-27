from fastapi import FastAPI, APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.templating import Jinja2Templates
import asyncio

class AgentsApi:
    def __init__(self):
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="templates")
        self.router.add_api_route("/", self.read_root, methods=["GET"])
        self.router.add_api_route("/healthcheck/", self.healthcheck, methods=["GET"])

    
    async def read_root(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})
    
    def healthcheck(self):
        return 'Health - OK'