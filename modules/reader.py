import json

import google.generativeai as genai

GEMINI_MODEL = "gemini-2.5-flash"

PROMPT = """Kamu dikasih sebuah gambar struk belanja.
Baca isinya dan keluarkan dalam format JSON seperti ini:
{
  "items": [
    {"name": "nama item", "count": 1, "total_price": 50000}
  ],
  "total": 50000
}

Aturan:
- total_price = harga total untuk item itu (bukan harga satuan)
- count = jumlah item, kalau di struk gak ada angkanya anggap 1
- total = total akhir struk (sudah termasuk pajak/service kalau ada)
- tulis angka tanpa titik atau koma pemisah ribuan, cukup angkanya saja
Keluarkan JSON-nya saja, jangan kasih penjelasan lain."""


def baca_struk(gambar, api_key):
    # set api key, siapin model, kirim prompt + gambar 
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content([PROMPT, gambar])

    teks = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(teks)
