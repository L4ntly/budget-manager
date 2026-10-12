from services.budget_manager import HarcamaYönetici
from models.expense import Harcama
import time

harcama1 = HarcamaYönetici()
harcama1.verileri_yukle()
print("UYGULAMA ÇALIŞIYOR.")

while True:
    print("="*40)
    print("KİŞİSEL BÜTÇE YÖNETİCİSİ")
    print("="*40)

    print("1. Bakiye")  
    print("2. Ürün Ekle") 
    print("3. Ürünleri Listele") 
    print("4. Ürün Sil")        
    print("5. Toplam Harcama")
    print("6. Ürün Ara")
    print("7. İstatistikler")  
    print("0. Çıkış")

    print("="*40)

    secim_yap = input("Lütfen Bir Seçim Yapınız: ")

    if secim_yap == "1":
        print(f"Bakiye: {harcama1.bakiye_goster()} TL")

    elif secim_yap == "2":
        try:
            id_al = int(input("ID: "))
            urun_al = input("Ürün: ")
            fiyat_al = float(input("Fiyat: "))
            kategori = input("Kategori: ")      

            harcama = Harcama(
                id_al,
                urun_al,
                fiyat_al,
                kategori
            )

            sonuc = harcama1.urun_ekle(harcama)
            print(sonuc)

            if sonuc == "Ürün Başarıyla Eklendi.":
                harcama1.verileri_kaydet()

        except ValueError:
            print("Hatalı giriş. ID sayı, fiyat ise sayısal bir değer olmalıdır.")
            
    elif secim_yap == "3":
        urunler = harcama1.urun_listele()

        if len(urunler) != 0:
            for i in urunler:
                print(
                    f"ID: {i.id} | "
                    f"Ürün: {i.urun} | "
                    f"Fiyat: {i.fiyat} TL | "
                    f"Kategori: {i.kategori}"
                )


    elif secim_yap == "4":
        harcama1.urun_sil()
        harcama1.verileri_kaydet()

    elif secim_yap == "5":
        print(f"Toplam Harcama: {harcama1.toplam_fiyat_hesapla()} TL")

    elif secim_yap == "6":
        sonuc = harcama1.urun_ara()

        if len(sonuc) != 0:
            for i in sonuc:
                print(
                    f"ID: {i.id} | "
                    f"Ürün: {i.urun} | "
                    f"Fiyat: {i.fiyat} TL | "
                    f"Kategori: {i.kategori}"
                )

    elif secim_yap == "7":
        harcama1.istatistikler()

    elif secim_yap == "0":
        print("Çıkış Yapılıyor...")
        time.sleep(2)
        break
    
    else:
        print("Hatalı seçim. Lütfen 0-7 arasında bir seçim yapınız.")
       


