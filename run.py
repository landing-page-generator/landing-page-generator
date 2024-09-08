import datetime
import os
import sys
from langchain_openai import ChatOpenAI

from git import Repo
from pathlib import Path
from dotenv import load_dotenv

_ = load_dotenv(Path(__file__).parent / '.env')


def main():
    # read idea from sys argv
    if len(sys.argv) < 2:
        print("Usage: python run.py <idea>")
        return
    idea = sys.argv[1]
    print('Idea:', idea)

    # init repo
    repo_url = 'git@github.com:landing-page-generator/landing-page-generator.github.io.git'
    repo_dir = 'landing-page-generator.github.io'
    if not os.path.exists(repo_dir):
        Repo.clone_from(repo_url, repo_dir)

    openai_api_key = os.environ['OPENAI_API_KEY']
    openai_model = os.environ.get('OPENAI_MODEL', 'gpt-4o-2024-05-13')
    llm = ChatOpenAI(model=openai_model, api_key=openai_api_key, temperature=0.6)

    print('AI model:', openai_model)
    prompt = (
        f'Create a landing page for a new product: "{idea}". '
        'Output ONLY html, without markdown or other formats.'
    )
    print('Prompt:', prompt)

    # call openai using langchain
    html_content = llm.invoke(prompt).content

    now = datetime.datetime.now().timestamp()
    filename = f'{now}.html'
    filepath = os.path.join(repo_dir, filename)
    print('File:', filepath)
    # write content to file
    with open(filepath, 'w') as f:
        f.write(html_content)
    # commit and push
    repo = Repo(repo_dir)
    repo.git.add(filename)
    repo.git.commit('-m', f'Add idea: {idea}')
    repo.git.push()
    print(f'URL: https://landing-page-generator.github.io/{filename}')
    print()


if __name__ == "__main__":
    main()