from .database import SessionLocal
import aiohttp
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
current_dir = os.path.dirname(os.path.realpath(__file__))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def send_emails(author: str, recipants: dict, thread_title: str, thread_url: str):
    tasks = []
    for (recipant, email) in recipants.items():
        tasks.append(send_email(email, author, recipant, thread_title, thread_url))

    await asyncio.gather(*tasks)

async def send_email(to_email: str, author: str, recipant: str, thread_title: str, thread_url: str):
    api_key = os.getenv("MAILGUN_API_KEY")
    if not api_key:
        return None

    try:
        html_template = read_file("../static/templates/template.html")
        html_template = html_template.replace("{{author}}", author) \
                                    .replace("{{recipants}}", recipant) \
                                    .replace("{{thread_title}}", thread_title) \
                                    .replace("{{thread_url}}", thread_url)
        
        async with aiohttp.ClientSession() as session:
            url = "https://api.mailgun.net/v3/sandbox2172160daa3b48128cb6d916fd06827d.mailgun.org/messages"
            auth = aiohttp.BasicAuth("api", api_key)
            data = {
            "from": "Email Sender<admin@sandbox2172160daa3b48128cb6d916fd06827d.mailgun.org>",
            "to": to_email,
            "subject": f"Check Out the Latest Thread: {thread_title}",
            "html": html_template
            }
            async with session.post(url, auth=auth, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    print(f"Error: {error_message}")
                    return {"error": error_message}
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_file(file_path: str):
    with open(os.path.join(current_dir, file_path), "r") as file:
        return file.read()
