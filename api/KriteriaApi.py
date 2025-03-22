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

# Add new kriteria
@router.post("/kriteria")

def add_kriteria(kriteria: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("INSERT INTO kriteria (nama, bobot) VALUES (%s, %s)", (kriteria["nama"], kriteria["bobot"]))
        conn.commit()

        return {"message": "Kriteria berhasil ditambahkan"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# Update kriteria by ID
@router.put("/kriteria/{id}")

def update_kriteria(id: int, kriteria: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("UPDATE kriteria SET nama = %s, bobot = %s WHERE id = %s", (kriteria["nama"], kriteria["bobot"], id))
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
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("DELETE FROM kriteria WHERE id = %s", (id,))
        conn.commit()

        return {"message": "Kriteria berhasil dihapus"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
