from fastapi import WebSocket, WebSocketException, status
from typing import List, Dict, Any, Union
from jose import jwt, JWTError
from app.core.config import settings
from app.api.dependencies import get_user_by_token

class ConnectionManager:

    def __init__(self):

        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, token: str):

        await websocket.accept()
        
        try:
            user = get_user_by_token(token)
            if not user:
                 raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid authentication token.")
            user_id = user.email
            
        except (JWTError, WebSocketException, Exception):
            # If authentication fails, close the connection
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Authentication failed.")
            return None
            

        self.active_connections[user_id] = websocket

        await self.send_personal_message({"type": "CONNECTION_SUCCESS", "message": f"Welcome, {user.role.value} dashboard user."}, user_id)
        
        return user_id

    def disconnect(self, user_id: str):

        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: Union[Dict, List], user_id: str):

        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except RuntimeError:
                print(f"Error sending message to {user_id}. Removing connection.")
                self.disconnect(user_id)


    async def broadcast(self, message: Union[Dict, List]):
        message_to_send = {"payload": message}
        
        for user_id, connection in list(self.active_connections.items()):
            try:
                await connection.send_json(message_to_send)
            except RuntimeError:
                
                print(f"Error broadcasting to {user_id}. Removing connection.")
                self.disconnect(user_id)
            except Exception as e:
                
                print(f"Unexpected error broadcasting to {user_id}: {e}")
                self.disconnect(user_id)


manager = ConnectionManager()
