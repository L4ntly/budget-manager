# Kişisel Harcama ve Bütçe Yöneticisi (Personal Expense & Budget Manager)

**Kişisel Harcama ve Bütçe Yöneticisi**, harcamaları sınıflandırarak takip etmeyi, bütçe limitlerini denetlemeyi, kategori bazlı harcama analizleri üretmeyi ve finansal verileri yerel olarak güvenle depolamayı sağlayan **Nesne Yönelimli Programlama (OOP)** ve **Veri Yapıları (Data Structures)** odaklı bir masaüstü / konsol uygulamasıdır.

Proje, yalnızca Python standart kütüphaneleri (`json`, `os`, `tkinter`, `time`, `sys`) kullanılarak modüler bir mimariyle geliştirilmiştir.

---

## 📌 İçindekiler
- [Proje Özeti & Temel Yetenekler]
- [Yazılım Mimarisi & Nesne Yönelimli Programlama (OOP)]
- [Veri Yapıları & Algoritmalar]
- [Veri Kalıcılığı (Persistence) & Güvenli Dosya Yönetimi]
- [Proje Dizin Ağacı (Directory Structure)]
- [Grafiksel Arayüz (GUI) Özellikleri]
- [Kurulum & Çalıştırma]

---

## 📖 Proje Özeti & Temel Yetenekler

Uygulama, bireysel finans yönetimini basitleştirmek ve verileri yapılandırılmış bir düzende işlemek amacıyla tasarlanmıştır. Sistem aşağıdaki temel yetenekleri sunar:

* **Bakiye & Limit Denetimi:** Her harcama öncesinde mevcut bakiye doğrulaması yapılır; bakiye yetersizse harcama engellenir. Varsayılan başlangıç bakiyesi `10.000 TL`'dir.
* **Harcama Kaydı & Bakiye İadesi:** Benzersiz ID, ürün adı, fiyat ve kategori bilgileriyle harcama kaydı yapılır. Silinen harcamaların tutarı otomatik olarak bakiyeye iade edilir.
* **Canlı Arama & Filtreleme:** Kayıtlı harcamalar arasında ürün adına veya kategoriye göre anlık doğrusal arama (linear search) ve filtreleme.
* **İstatistik & Raporlama:** En yüksek harcama, en düşük harcama, ortalama harcama tutarı ve kategori bazlı harcama dağılımı/yüzdeleri.
* **Fiyat Bazlı Sıralama:** Harcama listesinin fiyata göre artan veya azalan sırada dinamik olarak yeniden dizilmesi.
* **Çift Arayüz Desteği:** Hem terminal üzerinden çalışan interaktif CLI (`main.py`) hem de 200 satır altında optimize edilmiş modern, minimalist masaüstü GUI (`gui.py`) desteği.

---

## 🏗️ Yazılım Mimarisi & Nesne Yönelimli Programlama (OOP)

Proje, sorumlulukların ayrılığı (**Separation of Concerns**) prensibine uygun katmanlı bir mimari üzerinde inşa edilmiştir:

```text
┌─────────────────────────────────────────────────────────┐
│                    KULLANICI ARAYÜZÜ                    │
│        CLI (main.py)         │       GUI (gui.py)       │
└──────────────────────────────┬──────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────┐
│                      SERVİS KATMANI                     │
│               HarcamaYönetici (BudgetManager)           │
│  - Bakiye Doğrulama, Arama, Sıralama, İstatistik, I/O   │
└──────────────────────────────┬──────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────┐
│                      MODEL KATMANI                      │
│                  Harcama (Expense Entity)               │
│               - id, urun, fiyat, kategori               │
└──────────────────────────────┬──────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────┐
│                    KALICILIK KATMANI                    │
│                 JSON Storage (budget.json)              │
└─────────────────────────────────────────────────────────┘
```

### OOP Prensiplerinin Uygulanışı

1. **Varlık Modellemesi (Entity / Model):**
   - [`models/expense.py`] içerisindeki `Harcama` sınıfı, tek bir harcama kaydına ait tüm öznitelikleri (`id`, `urun`, `fiyat`, `kategori`) kapsüller.
   - `bilgileri_goster()` metodu ile nesne durumunu okunabilir şekilde konsola aktarır.

2. **İş Mantığı, Kapsülleme ve Kompozisyon (Encapsulation & Composition):**
   - [`services/budget_manager.py`] içerisindeki `HarcamaYönetici` sınıfı; harcamaların in-memory listesini (`self.harcamalar`), bakiye durumunu (`self.bakiye`), veri doğrulama kurallarını ve dosya işlemlerini kendi içerisinde kapsüller.
   - **Kompozisyon (Has-A İlişkisi):** `HarcamaYönetici` sınıfı, `Harcama` nesnelerinden oluşan dinamik bir listeyi (`self.harcamalar`) bünyesinde barındırarak yönetir.
   - Dış katmanlar doğrudan dosya I/O ile uğraşmaz; tüm işlemler bu servis sınıfı üzerinden yürütülür.

3. **Durum Yönetimi (State Management):**
   - Bakiye güncellemeleri, harcama ekleme anında eksiltme (`self.bakiye -= harcama.fiyat`) ve harcama silme anında iade (`self.bakiye += i.fiyat`) işlemleriyle tutarlı biçimde yönetilir.

4. **GUI Sınıf Mimarisi (`class BudgetApp`):**
   - [`gui.py`] dosyası, Tkinter arayüz bileşenlerini, olay dinleyicilerini (event handlers), form doğrulama mantığını ve `HarcamaYönetici` entegrasyonunu tek bir OOP sınıfı altında toplar.

---

## 📊 Veri Yapıları & Algoritmalar

| Veri Yapısı / Mantık | Kullanım Yeri | Açıklama |
| :--- | :--- | :--- |
| **Dinamik Liste (`List`)** | `self.harcamalar` | Harcama nesnelerinin bellekte ardışık ve dinamik olarak saklanması, filtrelenmesi ve taranması. |
| **Sözlük / Karma Tablo (`Dictionary / Hash Map`)** | `kategori_toplamlari`, `veri` | Kategorilere göre harcama toplamlarının O(1) ortalama erişimle toplanması ve JSON serialization structure. |
| **Doğrusal Arama (Linear Search & Filter)** | `urun_ara()`, Canlı Filtreleme | Liste üzerinde ürün adı veya ID eşleşmesini O(n) zaman karmaşıklığında bulan liste üreteci (list comprehension). |
| **Yerinde Sıralama (In-Place Sorting)** | `istatistikler()`, `_on_sort()` | Harcamaların fiyatlarına göre yerinde takas ile (Swap/Bubble & Timsort) küçükten büyüğe veya büyükten küçüğe sıralanması. |
| **Uç Değer ve Ortalama Analizi** | `toplam_fiyat_hesapla()`, `istatistikler()` | Toplam harcama, min-max karşılaştırmaları ve aritmetik ortalama hesaplamaları. |

---

## 💾 Veri Kalıcılığı (Persistence) & Güvenli Dosya Yönetimi

Veriler, program kapandığında kaybolmaması için `data/budget.json` dosyasına yazılır ve açılışta otomatik okunur:

```json
{
    "bakiye": 10000.0,
    "harcamalar": [
        {
            "id": 1,
            "urun": "Market Alışverişi",
            "fiyat": 450.0,
            "kategori": "Market"
        }
    ]
}
```

* **Serileştirme (Serialization):** Bellekteki `Harcama` nesneleri `to_dict` eşdeğeri Python sözlüklerine dönüştürülür ve `json.dump(veri, f, indent=4)` ile insan tarafından okunabilir (human-readable) biçimde diske yazılır.
* **Geri serileştirme (Deserialization):** Program açılışında `json.load(f)` ile JSON verisi okunur, sözlük kayıtları yeniden `Harcama(id, urun, fiyat, kategori)` nesnelerine dönüştürülerek nesne listesi ayağa kaldırılır.
* **Güvenli Dosya Kontrolü:** `os.path.exists("data/budget.json")` kontrolü ile dosyanın henüz var olmadığı ilk çalıştırma senaryoları `FileNotFoundError` hatasına düşmeden güvenle ele alınır.
* **Karakter Kodlaması:** Türkçe karakterlerin bozulmaması için tüm okuma ve yazma işlemlerinde standart `encoding="utf-8"` kullanılır.

---

## 📁 Proje Dizin Ağacı (Directory Structure)

```text
budget_manager/
│
├── data/
│   └── budget.json              # Kalıcı JSON veri tabanı (bakiye ve harcama kayıtları)
│
├── models/
│   ├── __init__.py              # Python paket tanımlayıcısı
│   └── expense.py               # Harcama veri varlık sınıfı (Harcama Modeli)
│
├── services/
│   ├── __init__.py              # Python paket tanımlayıcısı
│   └── budget_manager.py        # Harcama & Bütçe Yönetici servisi (İş mantığı ve I/O)
│
├── gui.py                       # Minimalist Tkinter Grafik Kullanıcı Arayüzü 
├── main.py                      # Terminal tabanlı interaktif Konsol Arayüzü (CLI)
└── README.md                    # Proje teknik dokümantasyonu
```



## 🖥️ Grafiksel Arayüz (GUI) Özellikleri

[`gui.py`] Modern masaüstü tasarım standartlarına göre tasarlanmış olup şu yetenekleri içerir:

1. **Özet Gösterge Kartları (Metric Cards):**
   * 💰 **Güncel Bakiye:** Pozitif zümrüt yeşili vurgu.
   * 💳 **Toplam Harcama:** Harcama tutarını gösteren kırmızı vurgu.
   * 📦 **Harcama Adedi:** Toplam kayıtlı item sayısı.
2. **Harcama Ekleme Formu:**
   * Otomatik ID öneri butonu ("Oto ID").
   * Ürün adı ve fiyat girişi (sayısal ve pozitiflik doğrulama).
   * Kategori açılır listesi (Combobox: Market, Yemek, Ulaşım, Fatura, vb.).
3. **Gelişmiş Harcama Tablosu (`ttk.Treeview`):**
   * Alternatif satır renklendirmesi (Zebra striping).
   * Harcama ID, Ürün, Kategori ve Fiyat (TL) sütunları.
   * **Canlı Arama:** Arama kutusuna yazıldıkça anında filtreleme.
   * **Fiyat Sıralama:** Tek tıkla artan veya azalan sıralama.
4. **İşlem & Analiz Araçları:**
   * 🗑️ **Seçili Harcamayı Sil:** Seçili kaydı siler, onay ister, tutarı bakiyeye iade eder ve kaydeder.
   * 📊 **İstatistikler & Rapor Modalı:** En pahalı, en ucuz, ortalama harcama tutarları ve kategori bazlı yüzdelik dağılım tablosu.
   * 💳 **Bakiye Ekleme / Güncelleme Modalı:** Mevcut bakiyeye para ekleme veya sıfırdan bütçe belirleme.

---

## 🚀 Kurulum & Çalıştırma

Proje standart Python kütüphaneleriyle yazıldığından ek bir paket kurulumuna (`pip install`) ihtiyaç duymaz.

### Gereksinimler
- **Python 3.8** veya daha üzeri bir sürüm.

### 1. Depoyu Klonlayın veya İndirin
```bash
git clone https://github.com/kullaniciadi/Personal-Expense-Budget-Manager.git
cd "Personal Expense & Budget Manager"
```

### 2. Grafiksel Arayüzü (GUI) Başlatma
Modern Tkinter masaüstü arayüzünü çalıştırmak için:
```bash
python gui.py
```

### 3. Konsol Arayüzünü (CLI) Başlatma
Terminal üzerinden çalışan metin tabanlı menüyü kullanmak için:
```bash
python main.py
```

---

## 🛡️ Lisans
Bu proje açık kaynaklıdır; eğitim ve kişisel kullanım amacıyla geliştirilmiştir.
