from fastapi import FastAPI, Request, Response
import uvicorn

app = FastAPI()
voice_mailbox = {}
sender_ids = {} # New dictionary to track who sent what

@app.post("/send-voice/{room_id}")
async def send_voice(room_id: str, request: Request):
    audio_data = await request.body()
    # Store the Sender-ID from the Unity Header
    sender_ids[room_id] = request.headers.get("Sender-ID", "")
    voice_mailbox[room_id] = audio_data
    return {"status": "sent"}

@app.get("/get-voice/{room_id}")
async def get_voice(room_id: str):
    if room_id in voice_mailbox:
        # Send the Sender-ID back to Unity so it can decide to play it or not
        return Response(
            content=voice_mailbox[room_id], 
            media_type="application/octet-stream",
            headers={"Sender-ID": sender_ids.get(room_id, "")}
        )
    return Response(status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
