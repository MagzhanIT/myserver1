from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow browser to access from any origin (important for public server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store the latest Arduino value
latest_data = {"value": 0}

@app.get("/")
def dashboard():
    html_content = """
    <html>
    <head>
        <title>Arduino Sensor Dashboard</title>
    </head>
    <body>
        <h1>Arduino Sensor Live Data</h1>
        <h2>Distance: <span id="value">0</span> cm</h2>

        <script>
            async function updateData() {
                try {
                    const response = await fetch('/latest');
                    const data = await response.json();
                    document.getElementById('value').innerText = data.value;
                } catch (err) {
                    console.log('Error fetching data:', err);
                }
            }

            // Update every 1 second
            setInterval(updateData, 1000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/latest")
def get_latest():
    # Return the latest value as JSON
    return latest_data

@app.post("/data")
def receive_data(data: dict):
    global latest_data
    latest_data = data
    return {"status": "ok", "received": data}
