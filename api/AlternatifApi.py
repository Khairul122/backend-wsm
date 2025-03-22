from fastapi import APIRouter, HTTPException
from conn import get_connection
from pydantic import BaseModel
import pymysql

router = APIRouter()

# ✅ Model Pydantic untuk request
class AlternatifRequest(BaseModel):
    nama_siswa: str
    NISN: str
    jenis_kelamin: str
    kelas: str  # ⬅️ Tambahkan field kelas

# ✅ GET all alternatif
@router.get("/alternatif")
def get_all_alternatif():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM alternatif")
        result = cursor.fetchall()

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ✅ GET by ID
@router.get("/alternatif/{id}")
def get_alternatif_by_id(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM alternatif WHERE id_alternatif = %s", (id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Data tidak ditemukan")

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ✅ POST add alternatif
@router.post("/alternatif")
def add_alternatif(data: AlternatifRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO alternatif (nama_siswa, NISN, jenis_kelamin, kelas)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (data.nama_siswa, data.NISN, data.jenis_kelamin, data.kelas))
        conn.commit()

        return {"message": "Data alternatif berhasil ditambahkan"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ✅ PUT update alternatif
@router.put("/alternatif/{id}")
def update_alternatif(id: int, data: AlternatifRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE alternatif
            SET nama_siswa = %s, NISN = %s, jenis_kelamin = %s, kelas = %s
            WHERE id_alternatif = %s
        """
        cursor.execute(sql, (data.nama_siswa, data.NISN, data.jenis_kelamin, data.kelas, id))
        conn.commit()

        return {"message": "Data alternatif berhasil diperbarui"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ✅ DELETE alternatif
@router.delete("/alternatif/{id}")
def delete_alternatif(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM alternatif WHERE id_alternatif = %s", (id,))
        conn.commit()

        return {"message": "Data alternatif berhasil dihapus"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
