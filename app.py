from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from simulation import simulation

app = FastAPI(title="AstraBots")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start")
async def start_simulation():
    asyncio.create_task(simulation.run())
    return {"status": "started"}

@app.post("/reset")
async def reset_simulation():
    simulation.reset()
    return {"status": "reset"}

@app.get("/state")
async def get_state():
    return simulation.get_state()
