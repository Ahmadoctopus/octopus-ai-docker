
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# السماح بالوصول من أي مكان (هام لتشغيله من أي جهاز في العالم)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stored_keys = {"api_key": "", "api_secret": ""}

@app.post("/set_keys")
def set_keys(api_key: str = Form(...), api_secret: str = Form(...)):
    stored_keys["api_key"] = api_key
    stored_keys["api_secret"] = api_secret
    print("✅ Received API Keys")
    return {"message": "Keys received"}

@app.post("/trade")
def start_trading():
    if not stored_keys["api_key"] or not stored_keys["api_secret"]:
        return {"error": "Keys not set"}
    print("✅ AI Trading started!")
    return {"message": "Trading started"}
