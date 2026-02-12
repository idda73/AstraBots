from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from simulation import SimulationEngine

app = FastAPI()
templates = Jinja2Templates(directory="templates")

engine = SimulationEngine()

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start")
def start_simulation():
    engine.start()
    return {"status": "started"}

@app.post("/reset")
def reset_simulation():
    engine.reset()
    return {"status": "reset"}

@app.get("/state")
def get_state():
    return JSONResponse(engine.get_state())
