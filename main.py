import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from run import generate_landing

app = FastAPI()


class InputData(BaseModel):
    idea: str
    existingContent: str | None = None
    email: EmailStr


@app.get('/', response_class=HTMLResponse)
async def read_index():
    with open('static/index.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content)


@app.post('/api/v1/subscribe')
async def subscribe_email(request: Request):
    try:
        form_data = await request.form()
        page_url = form_data.get('page_url')
        email = form_data.get('email')

        # Assuming you have a Supabase client set up
        from supabase import create_client, Client
        import os

        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)

        # Insert the email and page_url into Supabase
        data = supabase.table('leads').insert({"page_url": page_url, "lead_email": email}).execute()

        return HTMLResponse("<html><body><h1>Subscription successful</h1></body></html>")
    except Exception as e:
        return HTMLResponse(f"<html><body><h1>Error: {str(e)}</h1></body></html>")


@app.post('/api/v1/generate')
async def generate_landing_api(input_data: InputData):
    idea = input_data.idea
    existing_page = input_data.existingContent
    email = input_data.email  # Assuming you've added an email field to InputData

    try:
        url = generate_landing(idea, existing_page)

        # Save email and URL to Supabase
        from supabase import create_client, Client
        import os

        supabase_url: str = os.environ.get("SUPABASE_URL")
        supabase_key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)

        supabase.table('pages').insert({"page_url": url, "author_email": email}).execute()

        return {'url': url, 'message': 'Please wait a minute while it\'s deployed.'}
    except Exception as e:
        return {'url': '', 'message': 'Exception:' + str(e)}



if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)