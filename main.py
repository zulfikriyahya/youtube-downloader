import yt_dlp
import os
from colorama import Fore, Style, init

init(autoreset=True)

def garis():
    print(Fore.CYAN + "─" * 60 + Style.RESET_ALL)


def progress_hook(d):
    """Menampilkan progress bar download"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        print(Fore.YELLOW + f"\r📥 {percent} | ⚡ {speed} | ⏱ ETA {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print(Fore.GREEN + "\rDownload selesai!                     ")


def download_video(url, folder='hasil', only_audio=False):
    """Mengunduh satu video YouTube"""
    try:
        os.makedirs(folder, exist_ok=True)

        # Opsi dasar
        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4'
        }

        if only_audio:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'merge_output_format': None
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
            })

        print(Fore.YELLOW + f"\n📹 Mengunduh: {url}\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(Fore.GREEN + "\nVideo selesai diunduh!\n")

    except Exception as e:
        print(Fore.RED + f"\nGagal mengunduh {url}: {e}")


def download_playlist(playlist_url, folder='hasil', only_audio=False):
    """Mengunduh semua video dalam playlist"""
    try:
        os.makedirs(folder, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(playlist_title)s/%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True
        }

        if only_audio:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

        print(Fore.MAGENTA + f"\nMengunduh playlist: {playlist_url}\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

        print(Fore.GREEN + "\nSemua video dalam playlist selesai diunduh!\n")

    except Exception as e:
        print(Fore.RED + f"\nTerjadi kesalahan pada playlist: {e}")


if __name__ == "__main__":
    garis()
    print(Fore.CYAN + Style.BRIGHT + "YouTube Downloader")
    garis()

    url = input(Fore.WHITE + "Masukkan URL YouTube (video atau playlist): ").strip()
    mode = input(Fore.WHITE + "Ingin unduh (v)ideo atau (a)udio saja? [v/a]: ").lower()
    folder = input(Fore.WHITE + "Masukkan nama folder penyimpanan (default: hasil): ").strip() or "hasil"

    garis()

    only_audio = mode == 'a'

    if "playlist" in url.lower() or "list=" in url:
        download_playlist(url, folder=folder, only_audio=only_audio)
    else:
        download_video(url, folder=folder, only_audio=only_audio)

    garis()
    print(Fore.CYAN + "Terima kasih telah menggunakan YouTube Downloader")
    garis()
