import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from whitenoise import WhiteNoise
from pydantic import BaseModel
from run import generate_landing

app = FastAPI()

app.add_middleware(WhiteNoise, root="static", prefix="/static")

class InputData(BaseModel):
    idea: str


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content)


@app.post('/api/v1/generate')
async def generate_landing_api(input_data: InputData):
    idea = input_data.idea
    url = generate_landing(idea)
    return {'url': url}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)