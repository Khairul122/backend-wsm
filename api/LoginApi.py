from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from conn import get_connection  
import pymysql

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (request.username,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Username tidak ditemukan")
        if user["password"] != request.password:
            raise HTTPException(status_code=401, detail="Password salah")

        return {"message": f"Selamat datang, {user['username']}!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
