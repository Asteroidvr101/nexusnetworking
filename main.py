from fastapi import FastAPI, Request, Response
from mangum import Mangum
import uvicorn

app = FastAPI()
voice_mailbox = {}

@app.get("/")
async def root():
    return {"message": "Nexus Voice Relay is Online!", "status": "running"}

@app.post("/send-voice/{room_id}")
async def send_voice(room_id: str, request: Request):
    audio_data = await request.body()
    if audio_data:
        voice_mailbox[room_id] = audio_data
        return {"status": "sent"}
    return {"status": "error", "message": "no data"}

@app.get("/get-voice/{room_id}")
async def get_voice(room_id: str):
    if room_id in voice_mailbox:
        return Response(content=voice_mailbox[room_id], media_type="application/octet-stream")
    return Response(status_code=404)

if __name__ == "__main__":
    # Render uses port 10000 by default for free services
    uvicorn.run(app, host="0.0.0.0", port=10000)
