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

- `attachments/api.py` - original FastAPI script provided for reference
- `attachments/telegram_util.py` - original Pyrogram wrapper provided for reference
- `api.py` - fixed FastAPI script
- `telegram_util.py` - fixed Pyrogram wrapper
- `scripts/generate_session_string.py` - helper for creating a Pyrogram session string for Render
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies

## Testing Notes

The code can be syntax-checked without Telegram credentials:

```bash
python3 -m py_compile api.py telegram_util.py scripts/generate_session_string.py
```

Full runtime testing must be done by someone with valid Telegram credentials. The app requires:

```text
TELEGRAM_API_ID
TELEGRAM_API_HASH
```

For hosted environments such as Render, also provide:

```text
TELEGRAM_SESSION_STRING
```

Expected test results:

- Starting the API should connect the Pyrogram client without startup errors.
- `GET /test_telegram` should return a JSON array of recent chat message text.
- Sending a new message to a Telegram chat visible to the logged-in account should call `handle_message`.
- The new message should be printed and logged by the server process.
- Stopping the API should cleanly stop the Pyrogram client.

Without real credentials and an authorized Telegram session, the live connection, chat history endpoint, and incoming message handler cannot be verified locally.

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
uvicorn api:app --host 0.0.0.0 --port 8000
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
uvicorn api:app --host 0.0.0.0 --port $PORT
```

After deployment, test:

```bash
curl https://your-render-url.onrender.com/test_telegram
```

Note: Render Free web services can spin down when idle, which stops the Telegram message monitor until the service wakes up again. Use an always-on instance if continuous Telegram monitoring is required.
