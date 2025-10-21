from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware 
from app.core.config import settings
from app.api import auth ,requests,feedback
from app.api.endpoints import setup
import uvicorn

from app.core.websocket_manager import manager 

app = FastAPI(title="Bareez Hotel Dashboard")


origins = [

    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)



app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(requests.router, prefix="/api", tags=["requests"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])
app.include_router(setup.router, prefix="/api")


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
   
    token: str = Query(..., description="JWT for WebSocket authentication")
):
    
    user_id = await manager.connect(websocket, token)
    
    if user_id is None:
        
        return

 
    try:
        
        while True:
           
            await websocket.receive_text() 
            
    except WebSocketDisconnect:
       
        print(f"WS disconnected: {user_id}")
        manager.disconnect(user_id)
    except Exception as e:
        print(f"WS unexpected error for {user_id}: {e}")
        manager.disconnect(user_id)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)