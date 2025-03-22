from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Konfigurasi koneksi ke MySQL di Clever Cloud
db_config = {
    "host": "bex01irce3djnhpwjand-mysql.services.clever-cloud.com",
    "user": "uo8juyg29uxlsbav",
    "password": "0X733MLaud2qAcrzJCoB",
    "database": "bex01irce3djnhpwjand",
    "port": 3306
}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"message": "SPK WSM"}

@app.post("/login")
def login(request: LoginRequest):
    try:
        conn = pymysql.connect(**db_config)
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
