from fastapi import FastAPI, Request, Response
from mangum import Mangum
import uvicorn

app = FastAPI()
voice_mailbox = {}

@app.post("/send-voice/{room_id}")
async def send_voice(room_id: str, request: Request):
    audio_data = await request.body()
    voice_mailbox[room_id] = audio_data
    return {"status": "sent"}

@app.get("/get-voice/{room_id}")
async def get_voice(room_id: str):
    if room_id in voice_mailbox: # It only returns a 200 if this is TRUE
        return Response(content=voice_mailbox[room_id], ...)
    return Response(status_code=404) # Otherwise, it sends a 404

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
