from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .controllers.chat_controller import ChatController

app = FastAPI()
chat_controller = ChatController()

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, db: Session = Depends(get_db)):
    await chat_controller.connect(websocket, session_id, db)
    
    try:
        while True:
            data = await websocket.receive_json()
            response = await chat_controller.handle_message(data, session_id, db)
            await websocket.send_json(response)
    except WebSocketDisconnect:
        await chat_controller.disconnect(session_id, db)

@app.get("/messages/{session_id}")
async def get_messages(session_id: str, db: Session = Depends(get_db)):
    service = chat_controller.initialize_service(db)
    
    # Retrieve and return the session messages
    messages = await service.get_session_messages(session_id)
    return messages
