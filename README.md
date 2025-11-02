# YouTube Downloader (CLI)

Sebuah skrip Python sederhana untuk mengunduh video atau audio dari YouTube, baik secara individu maupun dalam bentuk playlist. Dibangun menggunakan [yt-dlp](https://github.com/yt-dlp/yt-dlp) dan menampilkan progress bar yang informatif dengan bantuan `colorama`.

---

## Fitur

- Unduh video YouTube dalam format MP4
- Unduh audio saja dalam format MP3 (320kbps)
- Dukungan untuk playlist YouTube
- Progress bar real-time (persentase, kecepatan, ETA)
- Output otomatis ke folder yang dapat dikustomisasi

---

## Instalasi

### 1. Clone repositori

```bash
git clone https://github.com/zulfikriyahya/youtube-downloader.git
cd youtube-downloader
```

### 2. Buat dan aktifkan virtual environment

```bash
python -m venv venv
# Aktifkan venv:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Cara Menjalankan

Jalankan skrip dengan Python:

```bash
python main.py
```

Ikuti instruksi di terminal:

1. Masukkan URL video atau playlist YouTube
2. Pilih mode unduhan: `(v)` untuk video atau `(a)` untuk audio saja
3. Masukkan nama folder penyimpanan (default: `hasil`)

---

## Struktur Output

- Video tunggal: `hasil/Nama Video.mp4`
- Audio tunggal: `hasil/Nama Video.mp3`
- Playlist video: `hasil/Nama Playlist/Nama Video.mp4`
- Playlist audio: `hasil/Nama Playlist/Nama Video.mp3`

---

## Catatan

- Pastikan `ffmpeg` sudah terinstal di sistem kamu. yt-dlp membutuhkannya untuk menggabungkan video dan audio atau mengekstrak audio.
- Jika belum terinstal, kamu bisa mengunduhnya dari [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Lisensi

Proyek ini bebas digunakan untuk keperluan pribadi. Pastikan untuk mematuhi ketentuan layanan YouTube saat menggunakan alat ini.
