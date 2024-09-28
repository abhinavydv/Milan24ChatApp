# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from routers import user, message
from config.db import engine, Base
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the SocketManager
socket_manager = SocketManager(app=app)

# Include your routers
app.include_router(user.router)
app.include_router(message.router)

# Add the Socket.IO event handlers here
@socket_manager.on('connect')
async def connect(sid, environ):
    print(f'Client connected: {sid}')

@socket_manager.on('join')
async def join(sid, data):
    user_id = data['user_id']
    await socket_manager.enter_room(sid, user_id)
    print(f'User {user_id} joined room {user_id}')

@socket_manager.on('disconnect')
async def disconnect(sid):
    print(f'Client disconnected: {sid}')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
