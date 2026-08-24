"""Personal Expense & Budget Manager - Minimalist Tkinter GUI"""
import os, sys, tkinter as tk
from tkinter import ttk, messagebox

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from models.expense import Harcama
from services.budget_manager import HarcamaYönetici

class BudgetApp:
    def __init__(self, root: tk.Tk):
        self.root, self.manager, self.sort_rev = root, HarcamaYönetici(), False
        self.root.title("Kişisel Bütçe ve Harcama Yöneticisi")
        self.root.geometry("960x650"); self.root.minsize(860, 560)
        self.manager.verileri_yukle()
        self.c = {"bg": "#0F172A", "card": "#1E293B", "border": "#334155", "txt": "#F8FAFC",
                  "sub": "#94A3B8", "blue": "#38BDF8", "green": "#34D399", "red": "#F87171"}
        self.root.configure(bg=self.c["bg"])
        self._init_ui()
        self._refresh()

    def _init_ui(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("Dark.TFrame", background=self.c["bg"])
        s.configure("Treeview", background=self.c["card"], foreground=self.c["txt"], fieldbackground=self.c["card"], font=("Segoe UI", 9), rowheight=26, borderwidth=0)
        s.configure("Treeview.Heading", background=self.c["border"], foreground=self.c["txt"], font=("Segoe UI", 9, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", "#2563EB")], foreground=[("selected", "#FFF")])

        m = ttk.Frame(self.root, style="Dark.TFrame", padding="16 12")
        m.pack(fill=tk.BOTH, expand=True)

        tk.Label(m, text="Personal Expense & Budget Manager", bg=self.c["bg"], fg=self.c["txt"], font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 8))

        # Metrics
        met = tk.Frame(m, bg=self.c["bg"]); met.pack(fill=tk.X, pady=(0, 8))
        met.columnconfigure((0, 1, 2), weight=1)
        self.cards = {}
        for col, (k, t, clr) in enumerate([("bal", "GÜNCEL BAKİYE", self.c["green"]), ("exp", "TOPLAM HARCAMA", self.c["red"]), ("cnt", "HARCAMA ADEDİ", self.c["blue"])]):
            f = tk.Frame(met, bg=self.c["card"], highlightbackground=self.c["border"], highlightthickness=1, padx=12, pady=6)
            f.grid(row=0, column=col, sticky="nsew", padx=3)
            tk.Label(f, text=t, bg=self.c["card"], fg=self.c["sub"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
            lbl = tk.Label(f, text="0.00 TL", bg=self.c["card"], fg=clr, font=("Segoe UI", 13, "bold"))
            lbl.pack(anchor="w"); self.cards[k] = lbl

        # Layout
        box = tk.Frame(m, bg=self.c["bg"]); box.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        box.columnconfigure(0, weight=3, minsize=240); box.columnconfigure(1, weight=7); box.rowconfigure(0, weight=1)

        # Form
        fp = tk.Frame(box, bg=self.c["card"], highlightbackground=self.c["border"], highlightthickness=1, padx=14, pady=10)
        fp.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(fp, text="Yeni Harcama Ekle", bg=self.c["card"], fg=self.c["txt"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))

        id_box = tk.Frame(fp, bg=self.c["card"]); id_box.pack(fill=tk.X, pady=(0, 4))
        tk.Label(id_box, text="ID:", bg=self.c["card"], fg=self.c["sub"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.ent_id = tk.Entry(id_box, bg=self.c["bg"], fg=self.c["txt"], insertbackground=self.c["txt"], relief="flat", highlightthickness=1, highlightbackground=self.c["border"])
        self.ent_id.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        tk.Button(id_box, text="Oto ID", command=self._auto_id, bg=self.c["border"], fg=self.c["txt"], relief="flat", font=("Segoe UI", 8), cursor="hand2").pack(side=tk.RIGHT, padx=(4, 0))

        self.entries = {}
        for fld, lbl_text in [("urun", "Ürün / Açıklama:"), ("fiyat", "Fiyat (TL):")]:
            tk.Label(fp, text=lbl_text, bg=self.c["card"], fg=self.c["sub"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
            e = tk.Entry(fp, bg=self.c["bg"], fg=self.c["txt"], insertbackground=self.c["txt"], relief="flat", highlightthickness=1, highlightbackground=self.c["border"])
            e.pack(fill=tk.X, pady=(0, 4), ipady=2); self.entries[fld] = e

        tk.Label(fp, text="Kategori:", bg=self.c["card"], fg=self.c["sub"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.cb_cat = ttk.Combobox(fp, values=["Market", "Yemek", "Ulaşım", "Fatura", "Eğlence", "Sağlık", "Eğitim", "Giyim", "Diğer"], state="normal")
        self.cb_cat.set("Market"); self.cb_cat.pack(fill=tk.X, pady=(0, 8))

        tk.Button(fp, text="➕ Harcama Ekle", command=self._on_add, bg=self.c["green"], fg="#0F172A", relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2", pady=4).pack(fill=tk.X, pady=(0, 3))
        tk.Button(fp, text="Formu Temizle", command=self._clear_form, bg=self.c["border"], fg=self.c["sub"], relief="flat", font=("Segoe UI", 8), cursor="hand2").pack(fill=tk.X, pady=(0, 6))
        tk.Button(fp, text="💳 Bakiye Güncelle", command=self._open_balance_dlg, bg=self.c["card"], fg=self.c["blue"], highlightthickness=1, highlightbackground=self.c["border"], relief="flat", font=("Segoe UI", 8, "bold"), cursor="hand2", pady=2).pack(fill=tk.X, side=tk.BOTTOM)

        # Table
        tp = tk.Frame(box, bg=self.c["card"], highlightbackground=self.c["border"], highlightthickness=1, padx=10, pady=8)
        tp.grid(row=0, column=1, sticky="nsew")

        tb_bar = tk.Frame(tp, bg=self.c["card"]); tb_bar.pack(fill=tk.X, pady=(0, 4))
        tk.Label(tb_bar, text="🔍 Ara:", bg=self.c["card"], fg=self.c["sub"], font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT, padx=(0, 4))
        self.srch_var = tk.StringVar(); self.srch_var.trace_add("write", lambda *_: self._refresh())
        tk.Entry(tb_bar, textvariable=self.srch_var, bg=self.c["bg"], fg=self.c["txt"], insertbackground=self.c["txt"], relief="flat", highlightthickness=1, highlightbackground=self.c["border"]).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=(0, 6))
        self.btn_sort = tk.Button(tb_bar, text="Fiyata Göre Sırala ⬍", command=self._on_sort, bg=self.c["border"], fg=self.c["txt"], relief="flat", font=("Segoe UI", 8), cursor="hand2", padx=6)
        self.btn_sort.pack(side=tk.RIGHT)

        tf = tk.Frame(tp, bg=self.c["card"]); tf.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(tf, columns=("id", "urun", "cat", "price"), show="headings", selectmode="browse")
        for col, (txt, w, anch) in [("id", ("ID", 50, "center")), ("urun", ("Ürün", 200, "w")), ("cat", ("Kategori", 100, "center")), ("price", ("Fiyat (TL)", 100, "e"))]:
            self.tree.heading(col, text=txt, anchor=anch); self.tree.column(col, width=w, anchor=anch)
        sc = ttk.Scrollbar(tf, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sc.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); sc.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.tag_configure("even", background="#1E293B"); self.tree.tag_configure("odd", background="#162032")

        # Bottom Bar
        bot = tk.Frame(m, bg=self.c["card"], highlightbackground=self.c["border"], highlightthickness=1, padx=8, pady=5)
        bot.pack(fill=tk.X)
        tk.Button(bot, text="🗑️ Harcamayı Sil", command=self._on_delete, bg=self.c["red"], fg="#0F172A", relief="flat", font=("Segoe UI", 8, "bold"), cursor="hand2", padx=6, pady=2).pack(side=tk.LEFT, padx=(0, 4))
        tk.Button(bot, text="📊 İstatistikler", command=self._open_stats_dlg, bg=self.c["border"], fg=self.c["txt"], relief="flat", font=("Segoe UI", 8), cursor="hand2", padx=6, pady=2).pack(side=tk.LEFT, padx=(0, 4))
        tk.Button(bot, text="💾 Kaydet", command=lambda: (self.manager.verileri_kaydet(), self._set_st("Kaydedildi.")), bg=self.c["border"], fg=self.c["txt"], relief="flat", font=("Segoe UI", 8), cursor="hand2", padx=6, pady=2).pack(side=tk.LEFT)
        self.lbl_st = tk.Label(bot, text="Hazır.", bg=self.c["card"], fg=self.c["blue"], font=("Segoe UI", 8))
        self.lbl_st.pack(side=tk.RIGHT)

    def _refresh(self):
        items = self.manager.urun_listele()
        q = self.srch_var.get().strip().lower()
        if q: items = [h for h in items if q in str(h.id).lower() or q in h.urun.lower() or q in h.kategori.lower()]
        self.cards["bal"].config(text=f"{self.manager.bakiye_goster():,.2f} TL")
        self.cards["exp"].config(text=f"{self.manager.toplam_fiyat_hesapla():,.2f} TL")
        self.cards["cnt"].config(text=f"{len(self.manager.urun_listele())} Kalem")
        self.tree.delete(*self.tree.get_children())
        for idx, h in enumerate(items):
            self.tree.insert("", tk.END, values=(h.id, h.urun, h.kategori, f"{float(h.fiyat):,.2f} TL"), tags=("even" if idx % 2 == 0 else "odd",))

    def _auto_id(self):
        items = self.manager.urun_listele()
        self.ent_id.delete(0, tk.END); self.ent_id.insert(0, str((max([h.id for h in items if isinstance(h.id, int)]) + 1) if items else 1))

    def _clear_form(self):
        self.ent_id.delete(0, tk.END)
        for e in self.entries.values(): e.delete(0, tk.END)
        self.cb_cat.set("Market")

    def _set_st(self, msg): self.lbl_st.config(text=msg)

    def _on_add(self):
        raw_id, urun, raw_f = self.ent_id.get().strip(), self.entries["urun"].get().strip(), self.entries["fiyat"].get().strip().replace(",", ".")
        cat = self.cb_cat.get().strip()
        if not (raw_id and urun and raw_f and cat): return messagebox.showwarning("Uyarı", "Tüm alanları doldurunuz.")
        try:
            h_id, f = int(raw_id), float(raw_f)
            if f <= 0: raise ValueError
        except ValueError: return messagebox.showerror("Hata", "ID tam sayı, fiyat pozitif sayı olmalıdır.")
        if any(h.id == h_id for h in self.manager.urun_listele()): return messagebox.showerror("Hata", f"ID {h_id} zaten kayıtlı.")
        if self.manager.urun_ekle(Harcama(h_id, urun, f, cat)) == "Ürün Başarıyla Eklendi.":
            self.manager.verileri_kaydet(); self._refresh(); self._clear_form(); self._set_st(f"'{urun}' eklendi.")
        else: messagebox.showwarning("Yetersiz Bakiye", f"Bakiye ({self.manager.bakiye_goster():.2f} TL) yetersiz!")

    def _on_delete(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showinfo("Bilgi", "Silinecek harcamayı seçiniz.")
        vals = self.tree.item(sel[0], "values")
        h_id, h_name = int(vals[0]), vals[1]
        if messagebox.askyesno("Silme Onayı", f"ID {h_id} ('{h_name}') silinsin mi?\nTutar bakiyeye iade edilecektir."):
            if self.manager.urun_sil(id_al=h_id):
                self.manager.verileri_kaydet(); self._refresh(); self._set_st(f"ID {h_id} silindi, tutar iade edildi.")

    def _on_sort(self):
        self.sort_rev = not self.sort_rev
        self.manager.urun_listele().sort(key=lambda x: x.fiyat, reverse=self.sort_rev)
        self.btn_sort.config(text=f"Sıralama: {'Azalan ⬇' if self.sort_rev else 'Artan ⬆'}"); self._refresh()

    def _open_balance_dlg(self):
        d = tk.Toplevel(self.root); d.title("Bakiye Güncelle"); d.geometry("320x190"); d.configure(bg=self.c["card"]); d.transient(self.root); d.grab_set()
        tk.Label(d, text="Bakiye Güncelle / Yükle", bg=self.c["card"], fg=self.c["txt"], font=("Segoe UI", 11, "bold")).pack(pady=8)
        tk.Label(d, text=f"Mevcut: {self.manager.bakiye_goster():,.2f} TL", bg=self.c["card"], fg=self.c["green"], font=("Segoe UI", 9, "bold")).pack()
        ent = tk.Entry(d, bg=self.c["bg"], fg=self.c["txt"], insertbackground=self.c["txt"], relief="flat", highlightthickness=1, highlightbackground=self.c["border"])
        ent.pack(fill=tk.X, padx=20, pady=8, ipady=2)
        btn_box = tk.Frame(d, bg=self.c["card"]); btn_box.pack(fill=tk.X, padx=20)
        def save(is_add):
            try:
                val = float(ent.get().replace(",", "."))
                if val <= 0 and is_add: return messagebox.showerror("Hata", "Tutar pozitif olmalı.", parent=d)
                self.manager.bakiye = (self.manager.bakiye + val) if is_add else val
                self.manager.verileri_kaydet(); self._refresh(); self._set_st("Bakiye güncellendi."); d.destroy()
            except ValueError: messagebox.showerror("Hata", "Geçerli sayı giriniz.", parent=d)
        tk.Button(btn_box, text="➕ Ekle", command=lambda: save(True), bg=self.c["green"], fg="#0F172A", relief="flat", font=("Segoe UI", 8, "bold"), cursor="hand2").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_box, text="🔄 Ayarla", command=lambda: save(False), bg=self.c["border"], fg=self.c["txt"], relief="flat", font=("Segoe UI", 8), cursor="hand2").pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)

    def _open_stats_dlg(self):
        items = self.manager.urun_listele()
        if not items: return messagebox.showinfo("İstatistik", "Analiz için harcama bulunamadı.")
        d = tk.Toplevel(self.root); d.title("İstatistik Raporu"); d.geometry("400x400"); d.configure(bg=self.c["card"]); d.transient(self.root); d.grab_set()
        tot = self.manager.toplam_fiyat_hesapla()
        pmax, pmin = max(items, key=lambda x: x.fiyat), min(items, key=lambda x: x.fiyat)
        cats = {}
        for h in items: cats[h.kategori] = cats.get(h.kategori, 0) + h.fiyat
        tk.Label(d, text="Bütçe & Harcama Raporu", bg=self.c["card"], fg=self.c["txt"], font=("Segoe UI", 11, "bold")).pack(pady=8)
        sf = tk.Frame(d, bg=self.c["bg"], highlightbackground=self.c["border"], highlightthickness=1, padx=10, pady=6); sf.pack(fill=tk.X, padx=12, pady=4)
        for idx, (k, v) in enumerate([("Toplam Harcama:", f"{tot:,.2f} TL"), ("Ortalama Harcama:", f"{tot/len(items):,.2f} TL"), ("En Yüksek:", f"{pmax.urun} ({pmax.fiyat:,.2f} TL)"), ("En Düşük:", f"{pmin.urun} ({pmin.fiyat:,.2f} TL)")]):
            tk.Label(sf, text=k, bg=self.c["bg"], fg=self.c["sub"], font=("Segoe UI", 8)).grid(row=idx, column=0, sticky="w", pady=1)
            tk.Label(sf, text=v, bg=self.c["bg"], fg=self.c["txt"], font=("Segoe UI", 8, "bold")).grid(row=idx, column=1, sticky="e", pady=1)
        sf.columnconfigure((0, 1), weight=1)
        tk.Label(d, text="Kategori Dağılımı", bg=self.c["card"], fg=self.c["txt"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(6, 2))
        cf = tk.Frame(d, bg=self.c["bg"], highlightbackground=self.c["border"], highlightthickness=1, padx=10, pady=6); cf.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        for r, (cat, val) in enumerate(sorted(cats.items(), key=lambda x: x[1], reverse=True)):
            pct = (val / tot) * 100 if tot else 0
            tk.Label(cf, text=f"• {cat}:", bg=self.c["bg"], fg=self.c["txt"], font=("Segoe UI", 8)).grid(row=r, column=0, sticky="w", pady=1)
            tk.Label(cf, text=f"{val:,.2f} TL (%{pct:.1f})", bg=self.c["bg"], fg=self.c["blue"], font=("Segoe UI", 8, "bold")).grid(row=r, column=1, sticky="e", pady=1)
        cf.columnconfigure((0, 1), weight=1)
        tk.Button(d, text="Kapat", command=d.destroy, bg=self.c["border"], fg=self.c["txt"], relief="flat", font=("Segoe UI", 8), cursor="hand2").pack(fill=tk.X, padx=12, pady=8)

if __name__ == "__main__":
    root = tk.Tk(); app = BudgetApp(root); root.mainloop()
