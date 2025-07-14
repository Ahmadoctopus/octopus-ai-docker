from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Octopus AI Docker Server is running ✅"}
