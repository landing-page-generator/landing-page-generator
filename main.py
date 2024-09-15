import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from run import generate_landing

app = FastAPI()


class InputData(BaseModel):
    idea: str


@app.get('/', response_class=HTMLResponse)
async def read_index():
    with open('static/index.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content)


@app.post('/api/v1/generate')
async def generate_landing_api(input_data: InputData):
    idea = input_data.idea
    try:
        url = generate_landing(idea)
        return {'url': url, 'message': 'Please wait a minute while it\'s deployed.'}
    except Exception as e:
        return {'url': '', 'message': 'Exception:' + str(e)}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)