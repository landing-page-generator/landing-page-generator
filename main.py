import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from run import generate_landing

app = FastAPI()


class InputData(BaseModel):
    idea: str
    existingContent: str | None = None


class SubscriptionData(BaseModel):
    page_url: str
    email: EmailStr


@app.get('/', response_class=HTMLResponse)
async def read_index():
    with open('static/index.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content)


@app.post('/api/v1/subscribe')
async def subscribe_email(subscription_data: SubscriptionData):
    try:
        # Assuming you have a Supabase client set up
        from supabase import create_client, Client
        import os

        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)

        # Insert the email and page_id into Supabase
        data = supabase.table('subscriptions').insert({"page_url": subscription_data.page_url, "email": subscription_data.email}).execute()

        return {"message": "Subscription successful"}
    except Exception as e:
        return {"error": str(e)}


@app.post('/api/v1/generate')
async def generate_landing_api(input_data: InputData):
    idea = input_data.idea
    existing_page = input_data.existingContent
    try:
        url = generate_landing(idea, existing_page)
        return {'url': url, 'message': 'Please wait a minute while it\'s deployed.'}
    except Exception as e:
        return {'url': '', 'message': 'Exception:' + str(e)}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)