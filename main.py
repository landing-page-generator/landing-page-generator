import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel
from run import generate_landing

app = FastAPI()


class InputData(BaseModel):
    idea: str


@app.get('/', response_class=HTMLResponse)
async def root():
    content = Path('ui/index.html').read_text()
    return content


@app.post('/api/v1/generate')
async def generate_landing_api(input_data: InputData):
    idea = input_data.idea
    url = generate_landing(idea)
    return {'url': url}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)