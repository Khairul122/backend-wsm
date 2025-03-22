from fastapi import APIRouter, HTTPException
from conn import get_connection
import pymysql

router = APIRouter()

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
