# Installation

```bash
cp .env.example .env
# add your OpenAI API key to .env
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

NB! Your machine should have push access to the repo `git@github.com:landing-page-generator/landing-page-generator.github.io.git`

# Run

```bash
python run.py 'My great idea'
```