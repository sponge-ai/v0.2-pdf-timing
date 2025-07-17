# README

Added print logging for response timing and time.txt journal.

```sh
# create virtual env
python3 -m venv .venv
source .venv/bin/activate

# install deps
pip install fastapi uvicorn python-multipart typing openai dotenv

# run server
uvicorn server:app --reload
```
