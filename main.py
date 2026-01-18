from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is public!"}

@app.post("/data")
def receive_data(data: dict):
    print("Received:", data)
    return {"status": "ok", "received": data}
