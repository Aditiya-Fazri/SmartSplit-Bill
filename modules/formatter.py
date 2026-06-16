def rupiah(angka):
    # ubah angka jadi format rupiah, contoh: 50000 -> "Rp 50.000"
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


def buat_ringkasan(hasil, total):
    # buat teks ringkasan buat didownload user
    baris = ["=== SmartSplit Bill ===", ""]
    for nama in hasil:
        detail = hasil[nama]
        baris.append(nama)
        for it in detail["items"]:
            baris.append("  - " + str(it["name"]) + " : " + rupiah(it["harga"]))
        baris.append("  Subtotal        : " + rupiah(detail["subtotal"]))
        baris.append("  Pajak & Service : " + rupiah(detail["extra"]))
        baris.append("  Total           : " + rupiah(detail["total"]))
        baris.append("")
    baris.append("Total semua orang : " + rupiah(total))
    return "\n".join(baris)
