from fastapi import APIRouter, HTTPException
from conn import get_connection
from pydantic import BaseModel
import pymysql

router = APIRouter()

# Pydantic model
class KriteriaRequest(BaseModel):
    kode_kriteria: str
    nama_kriteria: str
    bobot: float

# Get all kriteria
@router.get("/kriteria")
def get_all_kriteria():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM kriteria")
        result = cursor.fetchall()

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Get kriteria by ID
@router.get("/kriteria/{id}")
def get_kriteria_by_id(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM kriteria WHERE id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Kriteria tidak ditemukan")

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Add new kriteria
@router.post("/kriteria")
def add_kriteria(kriteria: KriteriaRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO kriteria (kode_kriteria, nama_kriteria, bobot) VALUES (%s, %s, %s)"
        cursor.execute(sql, (kriteria.kode_kriteria, kriteria.nama_kriteria, kriteria.bobot))
        conn.commit()

        return {"message": "Kriteria berhasil ditambahkan"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Update kriteria by ID
@router.put("/kriteria/{id}")
def update_kriteria(id: int, kriteria: KriteriaRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "UPDATE kriteria SET kode_kriteria = %s, nama_kriteria = %s, bobot = %s WHERE id = %s"
        cursor.execute(sql, (kriteria.kode_kriteria, kriteria.nama_kriteria, kriteria.bobot, id))
        conn.commit()

        return {"message": "Kriteria berhasil diperbarui"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Delete kriteria by ID
@router.delete("/kriteria/{id}")
def delete_kriteria(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM kriteria WHERE id = %s", (id,))
        conn.commit()

        return {"message": "Kriteria berhasil dihapus"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
