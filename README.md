# Landing Page Generator

One-button landing page generator -- transforms your idea into a live landing page in seconds.

Deployed at https://landing-page-generator-tau.vercel.app

Hacked on [Sundai](https://sundai.club), Sep 8, 2024

# Installation

```bash
cp .env.example .env
nano .env
# then add your GitHub and Gemini secret keys to the .env file
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run

## Command-line

```bash
python run.py 'My great idea'
```

## Local server

```bash
python main.py
```

or 

```bash
uvicorn main:app --reload
```

# Production deployment  

Auto deployed to Vercel https://landing-page-generator-tau.vercel.app at each commit to `main` branch.
