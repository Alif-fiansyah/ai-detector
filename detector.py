import os
import re
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[-] Error: GEMINI_API_KEY belum diatur di file .env")
    sys.exit(1)

client = genai.Client(api_key=api_key)


def hitung_statistik_teks(teks: str) -> dict:
    kalimat = [k.strip() for k in re.split(r"[.!?]+", teks) if k.strip()]
    if not kalimat:
        return {"total_kata": 0, "total_kalimat": 0, "variasi_panjang": 0.0}

    panjang_kalimat = [len(k.split()) for k in kalimat]
    total_kata = sum(panjang_kalimat)
    rata_rata = total_kata / len(kalimat)

    varians = sum((x - rata_rata) ** 2 for x in panjang_kalimat) / len(kalimat)
    standar_deviasi = varians ** 0.5

    return {
        "total_kata": total_kata,
        "total_kalimat": len(kalimat),
        "rata_rata_kata_per_kalimat": round(rata_rata, 1),
        "variasi_panjang": round(standar_deviasi, 2),
    }


class KalimatTerindikasi(BaseModel):
    kalimat: str = Field(description="Bagian kalimat yang terindikasi kental gaya AI")
    alasan: str = Field(description="Penyebab terindikasi, misalnya struktur monoton atau diksi klise")
    saran_parafrase: str = Field(description="Saran penulisan ulang agar lebih alami dan manusiawi")


class HasilDeteksi(BaseModel):
    skor_ai: int = Field(description="Estimasi probabilitas teks ditulis oleh AI dalam skala 0 sampai 100")
    tingkat_risiko: str = Field(description="Rendah, Sedang, atau Tinggi")
    ringkasan_analisis: str = Field(description="Penjelasan singkat mengenai karakteristik gaya penulisan teks")
    kalimat_terindikasi: list[KalimatTerindikasi] = Field(description="Daftar kalimat yang perlu diubah")


import time

def evaluasi_dengan_gemini(teks: str, statistik: dict) -> HasilDeteksi:
    prompt = f"""
    Kamu adalah seorang auditor penulisan akademik dan pakar analisis gaya teks.
    Tugasmu adalah menganalisis teks berikut untuk mendeteksi seberapa kuat indikasi keterlibatan AI dalam penyusunannya.

    Metrik statistik teks:
    - Total kata: {statistik['total_kata']}
    - Rata-rata kata per kalimat: {statistik['rata_rata_kata_per_kalimat']}
    - Variasi panjang kalimat: {statistik['variasi_panjang']}

    Fokus evaluasi pada ciri-ciri khas teks AI dalam bahasa Indonesia:
    1. Penggunaan kata sambung transisi yang berulang dan klise (misalnya: 'selain itu', 'oleh karena itu', 'dengan demikian', 'tidak dapat dimungkiri bahwa').
    2. Struktur kalimat yang terlalu simetris, monoton, dan minim gaya penulisan personal.
    3. Pernyataan umum yang berputar-putar tanpa langsung ke pokok inti bahasan.

    Teks untuk dianalisis:
    \"\"\"{teks}\"\"\"
    """

    # Daftar model cadangan jika model utama sedang sibuk
    daftar_model = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.0-flash"]

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=HasilDeteksi,
        temperature=0.2,
        tools=[],  # Menonaktifkan tool calling bawaan agar AFC warning tidak muncul
    )

    for nama_model in daftar_model:
        try:
            response = client.models.generate_content(
                model=nama_model,
                contents=prompt,
                config=config,
            )
            return HasilDeteksi.model_validate_json(response.text)
        except Exception as e:
            if "503" in str(e) or "404" in str(e):
                print(f"[-] Model {nama_model} sedang sibuk atau tidak tersedia. Mencoba alternatif...")
                time.sleep(1)
                continue
            raise e

    raise RuntimeError("Semua endpoint model Gemini sedang sibuk. Silakan coba 1-2 menit lagi.")


def main():
    print("=== PENDETEKSI TEKS AI & SARAN PARAFRASE ===")
    print("Masukkan teks tugas (akhiri dengan menekan Ctrl+D di baris baru):")
    print("-------------------------------------------------------------------")
    
    try:
        teks_input = sys.stdin.read().strip()
    except KeyboardInterrupt:
        return

    if len(teks_input) < 50:
        print("\n[-] Teks terlalu pendek untuk dianalisis. Masukkan minimal 1–2 paragraf.")
        return

    print("\n[*] Menghitung metrik statistik...")
    stat = hitung_statistik_teks(teks_input)

    print("[*] Menganalisis pola teks via Gemini...")
    hasil = evaluasi_dengan_gemini(teks_input, stat)

    print("\n=======================================================")
    print(f"📊 SKOR INDIKASI AI : {hasil.skor_ai}%")
    print(f"⚠️  TINGKAT RISIKO  : {hasil.tingkat_risiko}")
    print("=======================================================")
    print(f"\n[Statistik Teks]")
    print(f"- Total kata      : {stat['total_kata']}")
    print(f"- Total kalimat   : {stat['total_kalimat']}")
    print(f"- Variasi panjang : {stat['variasi_panjang']} (semakin rendah nilainya, semakin monoton/mirip AI)")

    print(f"\n[Analisis]")
    print(hasil.ringkasan_analisis)

    if hasil.kalimat_terindikasi:
        print(f"\n[Kalimat yang Perlu Diperbaiki ({len(hasil.kalimat_terindikasi)})]")
        for i, item in enumerate(hasil.kalimat_terindikasi, 1):
            print(f"\n{i}. Kalimat Asli : \"{item.kalimat}\"")
            print(f"   Alasan       : {item.alasan}")
            print(f"   Saran Ubah   : \"{item.saran_parafrase}\"")
    else:
        print("\n[+] Teks terdeteksi alami dan minim pola AI.")


if __name__ == "__main__":
    main()
