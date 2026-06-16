def hitung_subtotal(items):
    total = 0.0
    for i in range(len(items)):
        total = total + float(items[i]["total_price"])
    return total


def hitung_pembagian(items, assign, peserta, subtotal, total):
    hasil = {}
    for nama in peserta:
        hasil[nama] = {"items": [], "subtotal": 0.0, "extra": 0.0, "total": 0.0}

    # bagi tiap item ke orang yang dipilih
    for i in range(len(items)):
        harga_item = float(items[i]["total_price"])
        orang = assign.get(i, [])
        if len(orang) == 0:
            continue
        # jika 1 item dibayar lebih dari 1 orang, harganya dibagi rata
        bagian = harga_item / len(orang)
        for nama in orang:
            hasil[nama]["items"].append({"name": items[i]["name"], "harga": bagian})
            hasil[nama]["subtotal"] = hasil[nama]["subtotal"] + bagian


    for nama in peserta:
        sub = hasil[nama]["subtotal"]
        if subtotal > 0:
            tot = sub * (total / subtotal)
        else:
            tot = sub
        hasil[nama]["total"] = tot
        hasil[nama]["extra"] = tot - sub

    return hasil
