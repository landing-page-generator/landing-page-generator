import datetime
import os
import sys
from langchain_openai import ChatOpenAI

from github import Github
from github import Auth

from pathlib import Path
from dotenv import load_dotenv

_ = load_dotenv(Path(__file__).parent / '.env')


def generate_landing(idea: str) -> str:
    # init repo
    auth = Auth.Token(os.environ['GITHUB_ACCESS_TOKEN'])
    g = Github(auth=auth)
    repo = g.get_repo('landing-page-generator/landing-page-generator.github.io')

    openai_api_key = os.environ['OPENAI_API_KEY']
    openai_model = os.environ.get('OPENAI_MODEL', 'gpt-4o-2024-05-13')
    llm = ChatOpenAI(model=openai_model, api_key=openai_api_key, temperature=0.6)
    print('AI model:', openai_model)

    prompt = Path('prompts/first-version.txt').read_text()
    prompt = prompt.format(idea=idea)

    # call openai using langchain
    html_content = llm.invoke(prompt).content

    # deploy HTML page to github pages
    now = datetime.datetime.now().timestamp()
    filename = f'{now}.html'
    repo.create_file(
        path=filename,
        message=f'Add idea: {idea}',
        content=html_content,
        branch='main'
    )
    url = f'https://landing-page-generator.github.io/{filename}'
    print('URL:', url)
    print('Please wait a minute while it\'s deployed.')
    print()
    return url


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
