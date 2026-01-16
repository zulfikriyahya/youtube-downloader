import yt_dlp
import os
import time
import sys
import requests
import concurrent.futures
import pandas as pd
from colorama import Fore, Style, init
init(autoreset=True)

CHECK_URL = "https://www.google.com"
TIMEOUT = 8
MAX_THREADS = 10

class AnimatedUI:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def typewriter(text, color=Fore.WHITE, delay=0.02):
        for char in text:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def garis(length=60, color=Fore.CYAN):
        print(color + "═" * length + Style.RESET_ALL)
    
    @staticmethod
    def garis_double():
        print(Fore.CYAN + "╔" + "═" * 58 + "╗")
    
    @staticmethod
    def garis_double_bottom():
        print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    @staticmethod
    def box_text(text, color=Fore.CYAN):
        print(Fore.CYAN + "║ " + color + text.ljust(56) + Fore.CYAN + " ║")
    
    @staticmethod
    def loading_animation(text, duration=1):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{Fore.YELLOW}{frames[i % len(frames)]} {Fore.WHITE}{text}")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
        sys.stdout.write("\r" + " " * (len(text) + 3) + "\r")
        sys.stdout.flush()
    
    @staticmethod
    def banner():
        AnimatedUI.clear_screen()
        banner_art = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║                                                          ║
{Fore.CYAN}║ {Fore.YELLOW}███████╗███████╗██████╗ ██╗      █████╗ ██████╗ ███████╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}╚══███╔╝██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}  ███╔╝ █████╗  ██║  ██║██║     ███████║██████╔╝███████╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW} ███╔╝  ██╔══╝  ██║  ██║██║     ██╔══██║██╔══██╗╚════██║ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}███████╗███████╗██████╔╝███████╗██║  ██║██████╔╝███████║ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}╚══════╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ {Fore.CYAN}║
{Fore.CYAN}║                                                          ║
{Fore.CYAN}╠══════════════════════════════════════════════════════════╣
{Fore.CYAN}║   {Fore.GREEN}YouTube Downloader Pro v4.0 {Fore.CYAN}| {Fore.WHITE}Author: Yahya Zulfikri{Fore.CYAN}   ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝
        """
        print(banner_art)
        time.sleep(0.3)

def load_proxies(csv_file='proxy.csv'):
    """Load proxies dari CSV dengan pandas untuk performa lebih baik"""
    try:
        df = pd.read_csv(csv_file)
        
        if 'ip_address' in df.columns:
            proxies = df['ip_address'].dropna().astype(str).str.strip().tolist()
        else:
            proxies = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
        
        proxies = [f"http://{p}" if not p.startswith(('http://', 'https://', 'socks5://')) else p 
                   for p in proxies if p and not p.startswith('#')]
        
        proxies = list(set(proxies))
        
        if proxies:
            print(f"{Fore.GREEN}✓ {Fore.WHITE}Loaded {Fore.YELLOW}{len(proxies)}{Fore.WHITE} unique proxies")
        else:
            print(f"{Fore.YELLOW}⚠ {Fore.WHITE}No valid proxies found")
        
        return proxies
        
    except FileNotFoundError:
        print(f"{Fore.RED}✗ {Fore.WHITE}File {csv_file} not found")
        return []
    except Exception as e:
        print(f"{Fore.RED}✗ {Fore.WHITE}Error: {str(e)[:50]}")
        return []

def check_proxy(proxy):
    """Check single proxy dengan response time"""
    proxies_dict = {
        "http": proxy,
        "https": proxy,
    }
    try:
        start = time.time()
        response = requests.get(
            CHECK_URL, 
            proxies=proxies_dict, 
            timeout=TIMEOUT,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        if response.status_code == 200:
            latency = (time.time() - start) * 1000
            return {'proxy': proxy, 'latency': latency, 'status': 'OK'}
    except:
        pass
    return {'proxy': proxy, 'latency': 9999, 'status': 'FAIL'}

def test_all_proxies(proxies, max_workers=MAX_THREADS):
    """Test proxies dengan concurrent futures untuk speed maksimal"""
    
    print(f"\n{Fore.CYAN}╔{'═' * 58}╗")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}Testing {len(proxies)} proxies ({max_workers} threads){' ' * (58 - 28 - len(str(len(proxies))) - len(str(max_workers)))}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╠{'═' * 58}╣")
    
    AnimatedUI.loading_animation("Initializing ZEDLABS scanner...", 2.0)
    
    valid_proxies = []
    checked = 0
    total = len(proxies)
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            checked += 1
            
            if checked % 10 == 0 or checked == total:
                progress = int((checked / total) * 40)
                bar = "█" * progress + "░" * (40 - progress)
                percent = (checked / total) * 100
                sys.stdout.write(f"\r{Fore.CYAN}║{Fore.CYAN}[{Fore.YELLOW}{bar}{Fore.CYAN}] {Fore.WHITE}{percent:5.1f}% {Fore.CYAN}│ {Fore.WHITE}{checked}/{total} {Fore.CYAN}║")
                sys.stdout.flush()
            
            if result['status'] == 'OK':
                valid_proxies.append(result)
    
    print(f"\n{Fore.CYAN}╚{'═' * 58}╝")
    
    elapsed_time = time.time() - start_time
    
    AnimatedUI.loading_animation("Sorting by latency...", 0.5)
    
    if valid_proxies:
        valid_proxies.sort(key=lambda x: x['latency'])
        
        print(f"\n{Fore.GREEN}✓ {Fore.WHITE}Scan completed in {Fore.YELLOW}{elapsed_time:.2f}s")
        print(f"{Fore.GREEN}✓ {Fore.WHITE}Active proxies: {Fore.GREEN}{len(valid_proxies)}{Fore.WHITE}/{Fore.YELLOW}{total}")
        
        print(f"\n{Fore.CYAN}╔{'═' * 58}╗")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}Top 10 Fastest Proxies{' ' * 35}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═' * 58}╣")
        
        for i, p in enumerate(valid_proxies[:10], 1):
            proxy_short = p['proxy'].split('://')[-1][:28]
            latency_str = f"{p['latency']:.0f}ms"
            
            if p['latency'] < 500:
                speed_icon = f"{Fore.GREEN}⚡"
            elif p['latency'] < 1000:
                speed_icon = f"{Fore.YELLOW}●"
            else:
                speed_icon = f"{Fore.RED}◐"
            
            print(f"{Fore.CYAN}║ {Fore.YELLOW}{i:2d}. {speed_icon} {Fore.CYAN}{proxy_short:<28}            {Fore.YELLOW}{latency_str:>10} {Fore.CYAN}║")
        
        if len(valid_proxies) > 10:
            print(f"{Fore.CYAN}║ {Fore.WHITE}... +{len(valid_proxies) - 10} more proxies{' ' * (58 - 19 - len(str(len(valid_proxies) - 10)))}{Fore.CYAN}║")
        
        print(f"{Fore.CYAN}╚{'═' * 58}╝")
        
        return [p['proxy'] for p in valid_proxies]
    else:
        print(f"\n{Fore.RED}✗ No working proxies found")
        return []

def progress_hook(d):
    """Enhanced progress bar dengan warna dinamis"""
    if d['status'] == 'downloading':
        try:
            percent_str = d.get('_percent_str', '0%').strip()
            percent = float(percent_str.replace('%', ''))
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', 'N/A').strip()
            downloaded = d.get('_downloaded_bytes_str', 'N/A').strip()
            total = d.get('_total_bytes_str', 'N/A').strip()
            
            bar_length = 40
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            if percent < 25:
                color = Fore.RED
            elif percent < 50:
                color = Fore.YELLOW
            elif percent < 75:
                color = Fore.CYAN
            else:
                color = Fore.GREEN
            
            print(f"\r{Fore.CYAN}[{color}{bar}{Fore.CYAN}] {Fore.YELLOW}{percent:5.1f}% {Fore.CYAN}│ {Fore.WHITE}{speed:<10} {Fore.CYAN}│ {Fore.MAGENTA}ETA {eta:<8} {Fore.CYAN}│ {Fore.WHITE}{downloaded}/{total}", 
                  end='', flush=True)
        except:
            pass
    elif d['status'] == 'finished':
        print(f"\r{Fore.CYAN}[{Fore.GREEN}{'█' * 40}{Fore.CYAN}] {Fore.GREEN}100.0% {Fore.CYAN}│ {Fore.GREEN}Complete!{' ' * 40}")

def get_ydl_opts(folder, current_proxy, only_audio):
    """Optimized yt-dlp options untuk performa maksimal"""
    opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'retries': 10,
        'fragment_retries': 10,
        'socket_timeout': 30,
        'http_chunk_size': 10485760,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'concurrent_fragment_downloads': 5,
        'noplaylist': True,
    }
    
    if current_proxy:
        opts['proxy'] = current_proxy
    
    if only_audio:
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
    else:
        opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })
    
    return opts

def download_video(url, folder='hasil', only_audio=False, proxies=None):
    """Smart download dengan auto-fallback proxy"""
    os.makedirs(folder, exist_ok=True)
    
    proxy_index = 0
    max_attempts = min(len(proxies), 5) if proxies else 3
    
    for attempt in range(max_attempts):
        try:
            current_proxy = None
            if proxies and len(proxies) > proxy_index:
                current_proxy = proxies[proxy_index]
                proxy_short = current_proxy.split('://')[-1][:35]
                print(f"\n{Fore.CYAN}╔{'═' * 58}╗")
                print(f"{Fore.CYAN}║ {Fore.GREEN}Using proxy #{proxy_index + 1}: {Fore.YELLOW}{proxy_short:<32}{Fore.CYAN}║")
                print(f"{Fore.CYAN}╚{'═' * 58}╝")
            
            ydl_opts = get_ydl_opts(folder, current_proxy, only_audio)
            
            AnimatedUI.loading_animation("Establishing connection...", 0.8)
            print(f"{Fore.YELLOW}▶ {Fore.WHITE}Downloading: {Fore.CYAN}{url[:55]}...")
            print()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"\n{Fore.GREEN}✓ {Fore.WHITE}Download successful!\n")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n{Fore.RED}✗ {Fore.WHITE}Error: {error_msg[:55]}...")
            
            if proxies and proxy_index < len(proxies) - 1:
                proxy_index += 1
                print(f"{Fore.YELLOW}⟳ {Fore.WHITE}Switching to backup proxy #{proxy_index + 1}...")
                AnimatedUI.loading_animation("Reconnecting...", 0.8)
            else:
                print(f"\n{Fore.RED}✗ {Fore.WHITE}All proxies failed or download error")
                return False
    
    return False

def download_playlist(playlist_url, folder='hasil', only_audio=False, proxies=None):
    """Smart playlist download dengan error handling"""
    try:
        os.makedirs(folder, exist_ok=True)
        
        current_proxy = proxies[0] if proxies else None
        if current_proxy:
            proxy_short = current_proxy.split('://')[-1][:35]
            print(f"\n{Fore.GREEN}✓ {Fore.WHITE}Using fastest proxy: {Fore.YELLOW}{proxy_short}")
        
        ydl_opts = get_ydl_opts(folder, current_proxy, only_audio)
        ydl_opts['outtmpl'] = os.path.join(folder, '%(playlist_title)s/%(title)s.%(ext)s')
        ydl_opts['ignoreerrors'] = True
        ydl_opts['noplaylist'] = False
        
        AnimatedUI.loading_animation("Fetching playlist metadata...", 1)
        print(f"{Fore.MAGENTA}▶ {Fore.WHITE}Playlist: {Fore.CYAN}{playlist_url[:55]}...\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        
        print(f"\n{Fore.GREEN}✓ {Fore.WHITE}Playlist download complete!\n")
        return True
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ {Fore.WHITE}Error: {str(e)[:50]}")
        
        if proxies and len(proxies) > 1:
            print(f"{Fore.YELLOW}⟳ {Fore.WHITE}Retrying with backup proxy...")
            return download_playlist(playlist_url, folder, only_audio, proxies[1:])
        return False

def animated_input(prompt, color=Fore.CYAN):
    """Input dengan typewriter effect"""
    AnimatedUI.typewriter(prompt, color, delay=0.015)
    return input(f"{Fore.YELLOW}➜ {Fore.WHITE}")

if __name__ == "__main__":
    AnimatedUI.banner()
    
    AnimatedUI.garis_double()
    AnimatedUI.box_text("Configuration", Fore.YELLOW)
    AnimatedUI.garis_double_bottom()
    
    print()
    use_proxy = animated_input("Use proxy? [y/n]").lower()
    working_proxies = []
    
    if use_proxy == 'y':
        proxy_file = animated_input("Proxy CSV file (default: proxy.csv)") or "proxy.csv"
        
        AnimatedUI.loading_animation("Loading proxies...", 0.8)
        all_proxies = load_proxies(proxy_file)
        
        if all_proxies:
            time.sleep(0.3)
            working_proxies = test_all_proxies(all_proxies, max_workers=MAX_THREADS)
            
            if not working_proxies:
                print(f"\n{Fore.RED}✗ {Fore.WHITE}No working proxies, continuing without proxy\n")
                time.sleep(1)
    
    print()
    AnimatedUI.garis_double()
    AnimatedUI.box_text("Download Configuration", Fore.YELLOW)
    AnimatedUI.garis_double_bottom()
    print()
    
    url = animated_input("YouTube URL")
    mode = animated_input("Mode: (v)ideo or (a)udio? [v/a]").lower()
    folder = animated_input("Output folder (default: hasil)") or "hasil"
    
    only_audio = mode == 'a'
    
    print()
    AnimatedUI.garis(60, Fore.MAGENTA)
    AnimatedUI.loading_animation("Initializing ZEDLABS engine...", 1)
    
    if "playlist" in url.lower() or "list=" in url:
        download_playlist(url, folder=folder, only_audio=only_audio, proxies=working_proxies)
    else:
        download_video(url, folder=folder, only_audio=only_audio, proxies=working_proxies)
    
    print()
    AnimatedUI.garis_double()
    AnimatedUI.box_text("Process Complete - ZEDLABS", Fore.GREEN)
    AnimatedUI.garis_double_bottom()
    print()