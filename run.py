import datetime
import os
import sys
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from gemini import gemini

from github import Github
from github import Auth

from pathlib import Path
from dotenv import load_dotenv

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

_ = load_dotenv(Path(__file__).parent / '.env')

def send_email(to_email: str, subject: str, body_html: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(message)


def generate_landing(idea: str, existing_page: str) -> str:
    # init repo
    auth = Auth.Token(os.environ['GITHUB_ACCESS_TOKEN'])
    g = Github(auth=auth)
    repo = g.get_repo('landing-page-generator/landing-page-generator.github.io')

    # openai_api_key = os.environ['OPENAI_API_KEY']
    # openai_model = os.environ.get('OPENAI_MODEL', 'gpt-4o-2024-05-13')
    # llm = ChatOpenAI(model=openai_model, api_key=openai_api_key, temperature=0.6)
    # print('AI model:', openai_model)
    # gemini_api_key = os.environ['GEMINI_API_KEY']
    gemini_model = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')
    # llm = ChatGoogleGenerativeAI(model=gemini_model, api_key=gemini_api_key, temperature=0.6)
    print('AI model:', gemini_model)

    if existing_page:
        existing_page = '**Existing Page Example:**\n\n' + existing_page + '\n\n'
    else:
        existing_page = ''

    prompt = Path('prompts/master1-01-instructions.txt').read_text().replace('[[CONCEPT]]', idea).replace('[[EXISTING-PAGE]]', existing_page)
    prompt += Path('prompts/master1-02-rubric.txt').read_text()
    prompt += Path('prompts/master1-03-template.txt').read_text()
    # prompt = prompt.format(idea=idea)

    # call openai using langchain
    # html_content = llm.invoke(prompt).content
    html_content = gemini(prompt)

    # editor_prompt
    refine_prompt = Path('prompts/refine.txt').read_text() + f'\n{html_content}\n'
    refined_html_content = gemini(refine_prompt)
    refined_html_content = html_content

    # deploy HTML page to github pages
    now = datetime.datetime.now().timestamp()
    filename = f'{now}.html'
    repo.create_file(
        path=filename,
        message=f'Add idea: {idea}',
        content=refined_html_content,
        branch='main'
    )
    url = f'https://landing-page-generator.github.io/{filename}'
    print('URL:', url)
    print('Please wait a minute while it\'s deployed.')
    print()
    return url, refined_html_content


def generate_random_idea() -> str:
    prompt = "Generate a random, innovative AI startup idea in one sentence."
    idea = gemini(prompt)
    return idea.strip()


def main():
    # read idea from sys argv
    if len(sys.argv) < 2:
        print("Usage: python run.py <idea>")
        return
    idea = sys.argv[1]
    print('Idea:', idea)
    generate_landing(idea)


if __name__ == "__main__":
    main()
