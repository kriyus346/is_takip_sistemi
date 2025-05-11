import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime

projeler = []
calisanlar = []

def calisan_ekle():
    ad = simpledialog.askstring("Çalışan Ekle", "Çalışanın adı:")
    if ad:
        calisanlar.append({"ad": ad})
        messagebox.showinfo("Bilgi", f"{ad} adlı çalışan eklendi.")

def calisanlari_listele_str():
    return "\n".join(f"- {calisan['ad']}" for calisan in calisanlar) if calisanlar else "Henüz çalışan yok."

def proje_ekle():
    ad = simpledialog.askstring("Proje Ekle", "Proje adı:")
    if not ad:
        return
    aciklama = simpledialog.askstring("Proje Ekle", "Proje açıklaması:")

    while True:
        baslangic_tarihi_str = simpledialog.askstring("Proje Ekle", "Proje başlangıç tarihi (GG.AA.YYYY):")
        if not baslangic_tarihi_str:
            return
        try:
            baslangic_tarihi = datetime.strptime(baslangic_tarihi_str, "%d.%m.%Y").date()
            break
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen GG.AA.YYYY formatında girin.")

    while True:
        bitis_tarihi_str = simpledialog.askstring("Proje Ekle", "Proje bitiş tarihi (GG.AA.YYYY):")
        if not bitis_tarihi_str:
            return
        try:
            bitis_tarihi = datetime.strptime(bitis_tarihi_str, "%d.%m.%Y").date()
            if bitis_tarihi < baslangic_tarihi:
                messagebox.showerror("Hata", "Bitiş tarihi başlangıç tarihinden önce olamaz.")
            else:
                break
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen GG.AA.YYYY formatında girin.")

    projeler.append({
        "ad": ad,
        "aciklama": aciklama,
        "olusturma_tarihi": datetime.now().strftime("%d.%m.%Y"),
        "baslangic_tarihi": baslangic_tarihi.strftime("%d.%m.%Y"),
        "bitis_tarihi": bitis_tarihi.strftime("%d.%m.%Y"),
        "gorevler": []
    })
    messagebox.showinfo("Bilgi", f"{ad} adlı proje eklendi.")

def gorev_ekle():
    if not projeler:
        messagebox.showwarning("Uyarı", "Önce proje ekleyin.")
        return
    proje_secimi = simpledialog.askinteger("Görev Ekle", "\n".join(f"{i+1}. {p['ad']}" for i, p in enumerate(projeler)), minvalue=1, maxvalue=len(projeler))
    if proje_secimi is None:
        return
    proje = projeler[proje_secimi - 1]
    ad = simpledialog.askstring("Görev Ekle", "Görev adı:")
    if not ad:
        return
    aciklama = simpledialog.askstring("Görev Ekle", "Görev açıklaması:")
    proje['gorevler'].append({"ad": ad, "aciklama": aciklama, "durum": "Bekliyor", "olusturma_tarihi": datetime.now().strftime("%d.%m.%Y %H:%M"), "atanan_calisanlar": []})
    messagebox.showinfo("Bilgi", f"'{ad}' adlı görev '{proje['ad']}' projesine eklendi.")

def calisan_ata():
    if not projeler:
        messagebox.showwarning("Uyarı", "Önce proje ekleyin.")
        return
    proje_secimi = simpledialog.askinteger("Çalışan Ata", "\n".join(f"{i+1}. {p['ad']}" for i, p in enumerate(projeler)), minvalue=1, maxvalue=len(projeler))
    if proje_secimi is None:
        return
    proje = projeler[proje_secimi - 1]

    if not proje['gorevler']:
        messagebox.showwarning("Uyarı", f"'{proje['ad']}' projesinde henüz görev yok.")
        return
    gorev_secimi = simpledialog.askinteger("Çalışan Ata", "\n".join(f"{i+1}. {g['ad']}" for i, g in enumerate(proje['gorevler'])), minvalue=1, maxvalue=len(proje['gorevler']))
    if gorev_secimi is None:
        return
    gorev = proje['gorevler'][gorev_secimi - 1]

    if not calisanlar:
        messagebox.showwarning("Uyarı", "Henüz çalışan eklenmedi.")
        return
    calisan_secimi = simpledialog.askinteger("Çalışan Ata", f"Atanacak çalışanı seçin:\n{calisanlari_listele_str()}\nNumara:", minvalue=1, maxvalue=len(calisanlar))
    if calisan_secimi is None:
        return
    atanacak_calisan = calisanlar[calisan_secimi - 1]

    if atanacak_calisan in gorev['atanan_calisanlar']:
        messagebox.showwarning("Uyarı", f"{atanacak_calisan['ad']} zaten bu göreve atanmış.")
        return

    gorev['atanan_calisanlar'].append(atanacak_calisan)
    messagebox.showinfo("Bilgi", f"{atanacak_calisan['ad']} adlı çalışan '{proje['ad']}' projesindeki '{gorev['ad']}' görevine atandı.")

def ilerleme_kaydet():
    if not projeler:
        messagebox.showwarning("Uyarı", "Önce proje ekleyin.")
        return
    proje_secimi = simpledialog.askinteger("İlerleme Kaydet", "\n".join(f"{i+1}. {p['ad']}" for i, p in enumerate(projeler)), minvalue=1, maxvalue=len(projeler))
    if proje_secimi is None:
        return
    proje = projeler[proje_secimi - 1]
    if not proje['gorevler']:
        messagebox.showinfo("Bilgi", "Bu projede henüz görev yok.")
        return
    gorev_secimi = simpledialog.askinteger("İlerleme Kaydet", "\n".join(f"{i+1}. {g['ad']} ({g['durum']})" for i, g in enumerate(proje['gorevler'])), minvalue=1, maxvalue=len(proje['gorevler']))
    if gorev_secimi is None:
        return
    gorev = proje['gorevler'][gorev_secimi - 1]
    yeni_durum = simpledialog.askstring("İlerleme Kaydet", f"'{gorev['ad']}' için yeni durum (Bekliyor/Devam Ediyor/Tamamlandı):")
    if yeni_durum and yeni_durum in ["Bekliyor", "Devam Ediyor", "Tamamlandı"]:
        gorev['durum'] = yeni_durum
        messagebox.showinfo("Bilgi", "Durum güncellendi.")
    else:
        messagebox.showerror("Hata", "Geçersiz durum.")

def kayitlari_goster():
    if not projeler:
        messagebox.showinfo("Bilgi", "Henüz proje yok.")
        return
    txt = ""
    for p in projeler:
        txt += f"\nProje Adı: {p['ad']}\nAçıklama: {p['aciklama']}\nOluşturma Tarihi: {p['olusturma_tarihi']}\nBaşlangıç Tarihi: {p['baslangic_tarihi']}\nBitiş Tarihi: {p['bitis_tarihi']}\n--- Görevler ---"
        if p['gorevler']:
            for i, g in enumerate(p['gorevler']):
                txt += f"\n  {i+1}. Ad: {g['ad']}\n    Açıklama: {g['aciklama']}\n    Durum: {g['durum']}\n    Oluşturma Tarihi: {g['olusturma_tarihi']}"
                if g['atanan_calisanlar']:
                    txt += f"\n    Atanan Çalışanlar: {', '.join(c['ad'] for c in g['atanan_calisanlar'])}"
                else:
                    txt += "\n    Atanan Çalışan: Henüz atanmış çalışan yok."
                if g['durum'] == "Tamamlanmadı" and 'tamamlanmama_aciklamasi' in g and g['tamamlanmama_aciklamasi']:
                    txt += f"\n    Tamamlanmama Açıklaması: {g['tamamlanmama_aciklamasi']}"
        else:
            txt += "\n  Bu projede henüz görev yok."
        txt += "\n" + "-"*30
    pencere = tk.Toplevel()
    metin_alani = tk.Text(pencere)
    metin_alani.insert("1.0", txt)
    metin_alani.config(state="disabled")
    metin_alani.pack()

def proje_muduru_paneli():
    sifre = simpledialog.askstring("Proje Müdürü Girişi", "Proje Müdürü Şifresini Girin:", show='*')
    if sifre == "Ruhi123":
        pm_pencere = tk.Toplevel()
        pm_pencere.title("Proje Müdürü Paneli")

        proje_label = tk.Label(pm_pencere, text="Proje Seç:")
        proje_label.pack(pady=5)
        proje_listesi = ttk.Combobox(pm_pencere, values=[p['ad'] for p in projeler])
        proje_listesi.pack(pady=5)

        gorev_label = tk.Label(pm_pencere, text="Görev Seç:")
        gorev_label.pack(pady=5)
        gorev_listesi = ttk.Combobox(pm_pencere)
        gorev_listesi.pack(pady=5)

        def proje_secildi(event):
            secilen_proje_adi = proje_listesi.get()
            for p in projeler:
                if p['ad'] == secilen_proje_adi:
                    gorev_listesi['values'] = [g['ad'] for g in p['gorevler']]
                    break

        proje_listesi.bind("<<ComboboxSelected>>", proje_secildi)

        durum_label = tk.Label(pm_pencere, text="Yeni Durum:")
        durum_label.pack(pady=5)
        durum_combo = ttk.Combobox(pm_pencere, values=["Tamamlandı", "Tamamlanmadı"])
        durum_combo.pack(pady=5)

        aciklama_entry = None

        def durum_secildi(event):
            nonlocal aciklama_entry
            if durum_combo.get() == "Tamamlanmadı":
                if aciklama_entry is None:
                    aciklama_label = tk.Label(pm_pencere, text="Tamamlanmama Açıklaması:")
                    aciklama_label.pack(pady=5)
                    aciklama_entry = tk.Entry(pm_pencere)
                    aciklama_entry.pack(pady=5)
            elif aciklama_entry:
                aciklama_entry.destroy()
                aciklama_entry = None
                for widget in pm_pencere.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("text") == "Tamamlanmama Açıklaması:":
                        widget.destroy()
                pm_pencere.update_idletasks()

        durum_combo.bind("<<ComboboxSelected>>", durum_secildi)

        def gorev_durum_guncelle():
            secilen_proje_adi = proje_listesi.get()
            secilen_gorev_adi = gorev_listesi.get()
            yeni_durum = durum_combo.get()
            aciklama = aciklama_entry.get() if aciklama_entry else None

            if secilen_proje_adi and secilen_gorev_adi and yeni_durum:
                for p in projeler:
                    if p['ad'] == secilen_proje_adi:
                        for gorev in p['gorevler']:
                            if gorev['ad'] == secilen_gorev_adi:
                                gorev['durum'] = yeni_durum
                                gorev['tamamlanmama_aciklamasi'] = aciklama if yeni_durum == "Tamamlanmadı" else None
                                messagebox.showinfo("Bilgi", f"'{secilen_gorev_adi}' görevinin durumu '{yeni_durum}' olarak güncellendi.")
                                return
                messagebox.showerror("Hata", "Görev bulunamadı.")
            else:
                messagebox.showerror("Hata", "Lütfen proje, görev ve durumu seçin.")

        guncelle_button = tk.Button(pm_pencere, text="Görev Durumunu Güncelle", command=gorev_durum_guncelle)
        guncelle_button.pack(pady=10)

    else:
        messagebox.showerror("Hata", "Yanlış şifre.")
     
def baslat():
    p = tk.Tk()
    p.title("İş Takip Sistemi")
    for yazi, fonk in [
        ("Proje Ekle", proje_ekle),
        ("Görev Ekle", gorev_ekle),
        ("Çalışan Ekle", calisan_ekle),
        ("Çalışan Ata", calisan_ata),
        ("İlerleme Kaydet", ilerleme_kaydet),
        ("Kayıtları Gör", kayitlari_goster),
        ("Proje Müdürü Paneli", proje_muduru_paneli),
        ("Çık", p.quit)
    ]:
        tk.Button(p, text=yazi, command=fonk, width=15, height=2).pack(pady=8)
    p.mainloop()

if __name__ == "__main__":
    baslat()