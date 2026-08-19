class Harcama:
    def __init__(self,id,urun,fiyat,kategori):
        self.id = id
        self.urun = urun
        self.fiyat = fiyat
        self.kategori = kategori
       
        

    def bilgileri_goster(self):
        print("Ürün ID:", self.id)
        print("Ürün:", self.urun)
        print("Ürün Fiyatı(TL):", self.fiyat)
        print("Kategori:", self.kategori)
       

harcama = Harcama(1,"Food",750,"Market")
harcama.bilgileri_goster()

# i.id -> 1 
# i.urun -> "Food"
# i.miktar -> 750
# i.kategori -> "Market"
# i.tarih -> "16-08-2026"

