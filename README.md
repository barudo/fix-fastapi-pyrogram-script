# Fix my simple FastAPI/Pyrogram script

## Job Description

Hi. I'm attaching 2 files.

- `api.py` - FastAPI endpoint `/test_telegram`
- `telegram_util.py` - class that encapsulates Pyrogram

I want this to do 2 things:

1. Respond to the `/test_telegram` endpoint. This works.
2. Run normal Pyrogram message monitor and call `handle_message` for each new message. This does not work.

So I want to fix #2.

## Criteria

| ID | Description | Type |
| --- | --- | --- |
| 1 | `GET /test_telegram` endpoint returns chat history as JSON array | critical |
| 2 | Message handler (`handle_message`) triggers for new incoming Telegram messages | critical |
| 3 | Both API server and Telegram message monitoring run simultaneously without conflict | critical |
| 4 | Pyrogram client uses environment variables `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` | critical |
| 5 | Code runs without startup errors and maintains connection to Telegram | critical |
| 6 | Message handler prints or logs new messages when they arrive | optional |

## Files

- `attachments/api.py` - original FastAPI script
- `attachments/telegram_util.py` - original Pyrogram wrapper
- `attachments/api_fixed.py` - fixed FastAPI script
- `attachments/telegram_util_fixed.py` - fixed Pyrogram wrapper
- `scripts/generate_session_string.py` - helper for creating a Pyrogram session string for Render
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies

## Local Setup

Create Telegram API credentials at https://my.telegram.org.

Set the required environment variables:

```bash
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the fixed app:

```bash
cd attachments
uvicorn api_fixed:app --host 0.0.0.0 --port 8000
```

Test the endpoint:

```bash
curl http://localhost:8000/test_telegram
```

To test the message monitor, keep the server running and send a new Telegram message to an accessible chat. The fixed `handle_message` function should print/log the incoming message in the server terminal.

## Render Deployment

Render can run this as a web service, but the Telegram login must be handled with a session string. Do not rely on a local `.session` file on Render.

Generate the session string locally:

```bash
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
python scripts/generate_session_string.py
```

Copy the printed session string and add these environment variables in Render:

```text
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION_STRING=the_printed_session_string
```

The Render start command is defined in `render.yaml`:

```bash
cd attachments && uvicorn api_fixed:app --host 0.0.0.0 --port $PORT
```

After deployment, test:

```bash
curl https://your-render-url.onrender.com/test_telegram
```

Note: Render Free web services can spin down when idle, which stops the Telegram message monitor until the service wakes up again. Use an always-on instance if continuous Telegram monitoring is required.
