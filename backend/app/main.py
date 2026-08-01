from fastapi import FastAPI

app=FastAPI(
    title="Starting up",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Project Nexus"}

