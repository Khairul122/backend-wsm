from fastapi import APIRouter, HTTPException
from conn import get_connection
import pymysql

router = APIRouter()

@router.get("/proses-wsm")
def proses_perhitungan_wsm():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Ambil semua bobot kriteria
        cursor.execute("SELECT id, bobot FROM kriteria")
        kriteria_data = cursor.fetchall()
        bobot_map = {k['id']: float(k['bobot']) for k in kriteria_data}

        # Ambil semua alternatif
        cursor.execute("SELECT id_alternatif FROM alternatif")
        alternatif_data = cursor.fetchall()

        hasil = []

        for alt in alternatif_data:
            id_alternatif = alt['id_alternatif']
            total_nilai = 0

            # Ambil semua nilai penilaian alternatif ini
            cursor.execute("SELECT id_kriteria, nilai FROM penilaian WHERE id_alternatif = %s", (id_alternatif,))
            penilaian = cursor.fetchall()

            for p in penilaian:
                id_kriteria = p['id_kriteria']
                nilai = float(p['nilai'])
                bobot = bobot_map.get(id_kriteria, 0)
                total_nilai += nilai * bobot

            hasil.append({
                "id_alternatif": id_alternatif,
                "total_nilai": round(total_nilai, 4)
            })

        # Urutkan berdasarkan total_nilai (descending)
        hasil.sort(key=lambda x: x['total_nilai'], reverse=True)

        # Kosongkan isi tabel hasil
        cursor.execute("DELETE FROM hasil")

        # Masukkan hasil baru ke tabel hasil dengan ranking
        for rank, h in enumerate(hasil, start=1):
            cursor.execute(
                "INSERT INTO hasil (id_alternatif, total_nilai, rangking) VALUES (%s, %s, %s)",
                (h['id_alternatif'], h['total_nilai'], rank)
            )

        conn.commit()

        return {
            "message": "Perhitungan WSM berhasil dilakukan",
            "data": hasil
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
