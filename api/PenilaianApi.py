from fastapi import APIRouter, HTTPException
from conn import get_connection
from pydantic import BaseModel
import pymysql

router = APIRouter()

# Model request untuk insert/update
class PenilaianRequest(BaseModel):
    id_alternatif: int
    id_kriteria: int
    nilai: float

# GET: Semua penilaian (dengan join nama siswa dan nama kriteria)
@router.get("/penilaian")
def get_all_penilaian():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT 
            p.id_penilaian,
            p.id_alternatif,
            a.nama_siswa,
            p.id_kriteria,
            k.nama_kriteria,
            p.nilai
        FROM penilaian p
        JOIN alternatif a ON p.id_alternatif = a.id_alternatif
        JOIN kriteria k ON p.id_kriteria = k.id
        ORDER BY p.id_penilaian ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# GET: Penilaian berdasarkan alternatif (semua kriteria yang dinilai oleh siswa tersebut)
@router.get("/penilaian/{id_alternatif}")
def get_penilaian_by_alternatif(id_alternatif: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT 
            p.id_penilaian,
            p.id_kriteria,
            k.nama_kriteria,
            p.nilai
        FROM penilaian p
        JOIN kriteria k ON p.id_kriteria = k.id
        WHERE p.id_alternatif = %s
        ORDER BY p.id_kriteria
        """
        cursor.execute(query, (id_alternatif,))
        result = cursor.fetchall()

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# POST: Tambah penilaian
@router.post("/penilaian")
def add_penilaian(data: PenilaianRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Cegah duplikasi
        check = "SELECT * FROM penilaian WHERE id_alternatif = %s AND id_kriteria = %s"
        cursor.execute(check, (data.id_alternatif, data.id_kriteria))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Penilaian untuk alternatif dan kriteria ini sudah ada")

        query = """
        INSERT INTO penilaian (id_alternatif, id_kriteria, nilai)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data.id_alternatif, data.id_kriteria, data.nilai))
        conn.commit()

        return {"message": "Penilaian berhasil ditambahkan"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# PUT: Update penilaian
@router.put("/penilaian/{id_penilaian}")
def update_penilaian(id_penilaian: int, data: PenilaianRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE penilaian 
        SET id_alternatif = %s, id_kriteria = %s, nilai = %s
        WHERE id_penilaian = %s
        """
        cursor.execute(query, (data.id_alternatif, data.id_kriteria, data.nilai, id_penilaian))
        conn.commit()

        return {"message": "Penilaian berhasil diperbarui"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# DELETE: Hapus penilaian
@router.delete("/penilaian/{id_penilaian}")
def delete_penilaian(id_penilaian: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM penilaian WHERE id_penilaian = %s", (id_penilaian,))
        conn.commit()

        return {"message": "Penilaian berhasil dihapus"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
