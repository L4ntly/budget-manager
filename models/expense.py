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
       

if __name__ == "__main__":
    harcama = Harcama(1, "Food", 750, "Market")
    harcama.bilgileri_goster()

