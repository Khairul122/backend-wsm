from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Konfigurasi koneksi ke database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Ganti sesuai MySQL kamu
    "database": "db_wsm"
}

# Model input login
class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"message": "SPK WSM"}

@app.post("/login")
def login(request: LoginRequest):
    try:
        # Koneksi ke database
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Query cek user
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (request.username,))
        user = cursor.fetchone()

        # Cek hasil
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
