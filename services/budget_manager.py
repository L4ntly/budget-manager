import json
import os

from models.expense import Harcama

class HarcamaYönetici:
    def __init__(self):
        self.harcamalar = []
        self.bakiye = 10000


    def bakiye_goster(self):
        return self.bakiye


    def urun_ekle(self,harcama):
        if self.bakiye >= harcama.fiyat:
            self.harcamalar.append(harcama)
            self.bakiye -= harcama.fiyat
            return "Ürün Başarıyla Eklendi."
        else:
            return "Yetersiz Bakiye."
        

    def urun_listele(self):
        return self.harcamalar


    def urun_sil(self):
        
        try:
            id_al = int(input("ID: "))
            bulundu = False

            for i in self.harcamalar:                
                if id_al == i.id:
                    self.harcamalar.remove(i)
                    self.bakiye += i.fiyat
                    bulundu = True
                    break

            if bulundu == False:
                print("ID bulunamadı.")
            else:
                print("İşlem tamamlandı.")

        except ValueError:
            print(f"Hatalı Giriş: ID sayı olmalıdır.")
        
    
        
    def toplam_fiyat_hesapla(self):
        toplam = 0

        for i in self.harcamalar:
            toplam += i.fiyat

        return toplam

    def urun_ara(self):
        urun_ara = input("Ürün: ")
        sonuclar = [
            u for u in self.harcamalar 
            if urun_ara == u.urun
        ]
        return sonuclar


    def istatistikler(self):
        
        print("="*30)
        print("EN PAHALI ÜRÜN")

        if len(self.harcamalar) != 0:              
            en_yuksek = self.harcamalar[0]          

            for i in self.harcamalar:
                if i.fiyat > en_yuksek.fiyat:
                    en_yuksek = i

            print(f"En Pahalı Ürün: {en_yuksek.fiyat} TL")
        else:
            print("Henüz Ürün Bulunamıyor.")

        print("="*30)

        print("EN UCUZ ÜRÜN")

        if len(self.harcamalar) != 0:            
            en_dusuk = self.harcamalar[0]

            for i in self.harcamalar:
                if i.fiyat < en_dusuk.fiyat:
                    en_dusuk = i
            print(f"En Ucuz Ürün: {en_dusuk.fiyat} TL")
        else:
            print("Henüz Ürün Bulunamıyor.")



        
        print("="*30)
        print("ORTALAMA ÜRÜN FİYATI")
        if len(self.harcamalar) != 0:               
            ortalama = self.toplam_fiyat_hesapla() / len(self.harcamalar)
            print(f"Ortalama Ürün Fiyatı: {ortalama:.2f} TL")
        else:
            print("Henüz Ürün Bulunamıyor.")
        

        
        print("="*30)
        print("KATEGORİ BAZLI ÜRÜN ANALİZİ")
        kategori_toplamlari = {}
        if len(self.harcamalar) != 0:
            for i in self.harcamalar:
                if i.kategori in kategori_toplamlari:
                    kategori_toplamlari[i.kategori] += i.fiyat
                else:                    
                    kategori_toplamlari[i.kategori] = i.fiyat

            if kategori_toplamlari:
                for k, toplam in kategori_toplamlari.items():
                    print(f"{k}: {toplam} TL")
            else:
                print("Henüz Ürün Bulunamıyor.")
        


        print("="*30)
        print("ÜRÜNLERİN FİYATLARINI SIRALA")

        for i in range(len(self.harcamalar)):
            for j in range(len(self.harcamalar)):
                if self.harcamalar[i].fiyat < self.harcamalar[j].fiyat:
                    gecici = self.harcamalar[i]
                    self.harcamalar[i] = self.harcamalar[j]
                    self.harcamalar[j] = gecici
        print("="*30)
                


    def verileri_kaydet(self):
        print("="*30)
        print("VERİLERİ KAYDETME ALANI")

        kaydedilecek_harcamalar = []

        for i in self.harcamalar:
            harcama_verisi = {
                "id": i.id,
                "urun": i.urun,
                "fiyat": i.fiyat,
                "kategori": i.kategori
            }
                
            kaydedilecek_harcamalar.append(harcama_verisi)

        veri = {
            "bakiye": self.bakiye,
            "harcamalar": kaydedilecek_harcamalar           
        }


        with open("data/budget.json", "w", encoding="utf-8") as f:
            json.dump(veri, f, indent=4)

        print("Veriler Kaydedildi.")
        print("="*30)

    def verileri_yukle(self):
        print("="*30)
        print("VERİLERİ YÜKLEME ALANI")

        if os.path.exists("data/budget.json"):
            with open("data/budget.json", "r", encoding="utf-8") as f:
                veri = json.load(f)

                self.bakiye = veri["bakiye"]

                for i in veri["harcamalar"]:
                    harcama = Harcama(
                        i["id"],
                        i["urun"],
                        i["fiyat"],
                        i["kategori"]
                    )

                    self.harcamalar.append(harcama)
                print("Veriler Yüklendi.")
        else:
            print("Kayıtlı veri bulunamadı.")
        print("="*30)

        
    




            





        

            
# i -> o anki Harcama nesnesi
# self.miktar -> oluşturulan nesne miktarı
# i.id -> 1 
# i.urun -> "Food"
# i.miktar -> 750 yani harcama.miktar -> 750
# i.kategori -> "Market"
# i.tarih -> "16-08-2026"

# HarcamaYöneticisi
# │
# ├── self
# │
# └── self.harcamalar
#         │
#         ├── i → Harcama
#         │       ├── i.urun
#         │       ├── i.miktar
#         │       ├── i.kategori
#         │       └── i.tarih
#         │
#         ├── i → Harcama
#         └── i → Harcama