from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/set_keys")
async def set_keys(api_key: str = Form(...), api_secret: str = Form(...)):
    print("Received API Keys:", api_key, api_secret)
    return {"status": "ok"}

