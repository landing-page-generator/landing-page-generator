import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from run import generate_landing, generate_random_idea

app = FastAPI()


class InputData(BaseModel):
    idea: str
    existingContent: str | None = None
    email: str | None = None


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
        lead_email = form_data.get('email')

        from supabase import create_client, Client
        import os
        from run import send_email

        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)

        # Insert the email and page_url into Supabase
        data = supabase.table('leads').insert({"page_url": page_url, "lead_email": lead_email}).execute()

        # Get author_email for this page_url
        result = supabase.table('pages').select('author_email').eq('page_url', page_url).execute()
        if result.data:
            author_email = result.data[0]['author_email']
            # Send email to author about new signup
            subject = "[LPG] New Lead Signup"
            message_html = f"A new lead has signed up for your landing page: {page_url}<br><br>Lead's email: {lead_email}"
            send_email(author_email, subject, message_html)

        return HTMLResponse("<html><body><h1>Sign up successful! We will contact you.</h1></body></html>")
    except Exception as e:
        return HTMLResponse(f"<html><body><h1>Error: {str(e)}</h1></body></html>")


@app.post('/api/v1/generate')
async def generate_landing_api(input_data: InputData):
    idea = input_data.idea
    existing_page = input_data.existingContent
    author_email = input_data.email

    try:
        url = generate_landing(idea, existing_page)

        # Save email and URL to Supabase
        from supabase import create_client, Client
        import os

        supabase_url: str = os.environ.get("SUPABASE_URL")
        supabase_key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)

        supabase.table('pages').insert({"page_url": url, "author_email": author_email, "idea": idea, "existing_page_url": existing_page}).execute()

        return {'url': url, 'message': 'Please wait a minute while it\'s deployed.'}
    except Exception as e:
        return {'url': '', 'message': 'Exception:' + str(e)}


@app.get('/api/v1/random-idea')
async def get_random_idea():
    try:
        idea = generate_random_idea()
        return JSONResponse(content={"idea": idea})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)