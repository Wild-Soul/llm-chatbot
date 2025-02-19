from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas import ErrorResponse
from .logger import logger

# Before loading anything -- load env file
from dotenv import load_dotenv
load_dotenv()

from .database import get_db
from app.controllers import ChatController

app = FastAPI()
chat_controller = ChatController()

@app.websocket("/api/v1/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, db: Session = Depends(get_db)):
    await chat_controller.connect(websocket, session_id, db)
    logger.debug("Websocket connection request received, from session id: {}".format(session_id))
    
    # Create a websocket connection for sending and receiving messages.
    try:
        while True:
            try:
                data = await websocket.receive_json()
                logger.debug("Websocket: data: {}".format(data))
                response = await chat_controller.handle_message(data, session_id, db)
                logger.debug("Webscoket: Sending response: {}".format(response))
                await websocket.send_json(response)
            except Exception as e:
                logger.error("Websocket: Unhandled exception {}".format(e))
                await websocket.send_json({
                    "type": "failure",
                    "message": str(e)
                })
    except WebSocketDisconnect as e:
        logger.error("Websocket: Websocket connection disconnected:{}".format(str(e)))
        await chat_controller.disconnect(session_id, db)


@app.get("/api/v1/messages/{session_id}")
async def get_messages(session_id: str, db: Session = Depends(get_db)):
    logger.debug("Messages: Received request to retrieve all message for {}".format(session_id))
    try:
        service = chat_controller.initialize_service(db)
    
        # Retrieve and return the session messages
        messages = await service.get_session_messages(session_id)
        logger.debug("Sending response: {}".format(len(messages)))
        return messages
    except Exception as e:
        logger.error("Messages: Failed to get all message: {}".format(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    error_response = ErrorResponse(
        message=exc.detail,
        status_code=exc.status_code,
    )
    logger.error("Exception handled: {}".format(exc))
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump_json()
    )
