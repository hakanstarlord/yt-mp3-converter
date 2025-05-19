import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
import time

def download_and_convert():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Hata", "Lütfen bir YouTube URL'si gir.")
        return

    try:
        # Videonun başlığını al
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'output')

        # Dosya adını temizle (boşluklar ve garip karakterlerden arındır)
        sanitized_title = "".join(c for c in title if c.isalnum() or c in " -_").rstrip()
        download_dir = os.path.expanduser("~\\Downloads")
        save_path = os.path.join(download_dir, sanitized_title)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': save_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'verbose': True
        }

        # İndir ve gerçekte oluşturulan dosya adını al
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            actual_filename = ydl.prepare_filename(info_dict).rsplit('.', 1)[0] + ".mp3"

        actual_path = save_path if os.path.exists(save_path) else save_path + ".mp3"
        # Aç ve göster
        if os.path.exists(actual_filename):
            os.utime(actual_path, (time.time(), time.time()))
            os.startfile(actual_filename)
            messagebox.showinfo(
                "Başarılı",
                f"'{title}' adlı ses dosyası indirildi ve açıldı.\n\nKonum:\n{actual_filename}"
            )
        else:
            messagebox.showwarning(
                "Uyarı",
                f"Dosya indirildi ama bulunamıyor:\n{actual_filename}"
            )

    except Exception as e:
        messagebox.showerror("Hata", f"Bir şeyler ters gitti:\n{str(e)}")

# GUI
root = tk.Tk()
root.title("YouTube'dan Ses Dönüştürücü")
root.geometry("400x150")
root.resizable(False, False)

label = tk.Label(root, text="YouTube Video URL'sini gir:")
label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack()

convert_button = tk.Button(root, text="Ses Dosyasına Dönüştür", command=download_and_convert)
convert_button.pack(pady=20)

root.mainloop()
