# ZEDLABS YouTube Downloader

A high-performance Python CLI tool for downloading YouTube videos and audio with advanced proxy support. Built with yt-dlp and featuring an animated, colorful terminal interface.

![ZEDLABS YouTube Downloader](./proxy_mode.png)

---

## Features

### Core Functionality

- Download YouTube videos in MP4 format (best quality)
- Extract audio only in MP3 format (320kbps)
- Full playlist support with batch downloading
- Real-time progress bar with download statistics
- Customizable output folders with auto-organization

### Advanced Features

- **High-Performance Proxy System**: Test and use multiple proxies with automatic fallback
- **Concurrent Proxy Testing**: Test up to 10 proxies simultaneously
- **Smart Proxy Selection**: Automatically sorts and uses fastest proxies
- **Latency Monitoring**: Real-time proxy performance metrics
- **Auto-Retry Mechanism**: Seamless switching to backup proxies on failure
- **Animated Terminal UI**: Professional loading animations and progress indicators

### Performance Optimizations

- Concurrent fragment downloads (5 fragments simultaneously)
- Pandas-powered CSV parsing for faster proxy loading
- ThreadPoolExecutor for efficient multi-threading
- Optimized chunk sizes (10MB) for faster downloads
- Smart timeout management and retry logic

---

## Screenshots

### Single Video Mode

![Single Video/Audio Download](./single_mode.png)

### Playlist Mode

![Playlist Video/Audio Download](./playlist_mode.png)

### Proxy Mode

![Proxy System](./proxy_mode.png)

---

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system

### 1. Clone the repository

```bash
git clone https://github.com/zulfikriyahya/youtube-downloader.git
cd youtube-downloader
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv

# Activate virtual environment:
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

FFmpeg is required for merging video/audio streams and audio extraction.

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to PATH

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install ffmpeg
```

---

## Usage

### Basic Usage

Run the script:

```bash
python3 main.py
```

Follow the interactive prompts:

1. Choose whether to use proxy (y/n)
2. If using proxy, provide proxy CSV file path
3. Enter YouTube video or playlist URL
4. Select download mode: (v) for video or (a) for audio only
5. Specify output folder (default: hasil)

### Proxy Setup

Create a `proxy.csv` file with the following format:

```csv
ip_address
192.168.1.1:8080
10.0.0.1:3128
proxy.example.com:8888
```

The system will:

- Test all proxies concurrently (10 threads)
- Display latency for each proxy
- Sort by response time
- Use fastest proxy for downloads
- Auto-switch to backup proxies on failure

---

## Output Structure

### Single Videos

- Video: `hasil/Video_Title.mp4`
- Audio: `hasil/Video_Title.mp3`

### Playlists

- Video: `hasil/Playlist_Name/Video_Title.mp4`
- Audio: `hasil/Playlist_Name/Video_Title.mp3`

---

## Configuration

You can modify the following constants in `main.py`:

```python
CHECK_URL = "https://www.google.com"  # URL for proxy testing
TIMEOUT = 8                            # Proxy timeout in seconds
MAX_THREADS = 10                       # Concurrent proxy testing threads
```

---

## Dependencies

```
yt-dlp>=2024.0.0
colorama>=0.4.6
pandas>=2.0.0
requests>=2.31.0
```

---

## Troubleshooting

### Common Issues

**Error: FFmpeg not found**

- Ensure FFmpeg is installed and added to system PATH
- Restart terminal after installation

**Proxy connection errors**

- Verify proxy format in CSV (ip:port)
- Test proxy manually with curl or browser
- Some proxies may require authentication

**Download speed issues**

- Try using proxies with lower latency
- Reduce concurrent fragment downloads
- Check your internet connection

**SSL Certificate errors**

- Update yt-dlp: `pip install -U yt-dlp`
- Update certifi: `pip install -U certifi`

---

## Performance Tips

1. **Use Quality Proxies**: Free proxies are often slow or unreliable
2. **Increase Thread Count**: Modify MAX_THREADS for faster proxy testing
3. **Update yt-dlp**: Keep yt-dlp updated for best performance
4. **SSD Storage**: Download to SSD for faster write speeds
5. **Stable Connection**: Use wired connection for large downloads

---

## Legal Notice

This tool is for personal use only. Users are responsible for complying with YouTube's Terms of Service and copyright laws. Do not use this tool to download copyrighted content without permission.

---

## Author

**Yahya Zulfikri**

- GitHub: [@zulfikriyahya](https://github.com/zulfikriyahya)

---

## License

This project is open source and available for personal use. Please respect YouTube's Terms of Service and copyright regulations when using this tool.

---

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The core download engine
- [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal output
- [pandas](https://pandas.pydata.org/) - High-performance data structures

---

## Version History

### v4.0 (Current)

- Added high-performance proxy system
- Concurrent proxy testing with ThreadPoolExecutor
- Animated terminal UI with loading indicators
- Smart proxy selection and auto-fallback
- Performance optimizations for faster downloads
- Enhanced progress bar with dynamic colors

### v3.0

- Added playlist support
- Improved error handling
- Better progress tracking

### v2.0

- Added audio-only mode
- Customizable output folders
- Progress bar implementation

### v1.0

- Initial release
- Basic video download functionality

---

## Contributing

We welcome contributions to improve ZEDLABS YouTube Downloader! Here's how you can help:

### Reporting Issues

If you encounter bugs or have feature requests:

1. Check existing issues on GitHub to avoid duplicates
2. Provide detailed information about your system (OS, Python version)
3. Include error messages and logs
4. Describe steps to reproduce the issue

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature-name`
6. Submit a pull request with detailed description

### Code Standards

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test changes on multiple platforms when possible

---

## Roadmap

### Planned Features

- **v5.0 (Future)**
  - GUI interface with Tkinter
  - Resume interrupted downloads
  - Scheduled downloads
  - Download queue management
  - Browser extension integration
- **v4.5 (Next Release)**
  - SOCKS proxy support
  - Custom quality selection
  - Subtitle download support
  - Download history tracking
  - Configuration file support

---

## FAQ

**Q: Can I download entire channels?**  
A: Currently only playlist support is available. Full channel downloading will be added in future versions.

**Q: Does this work with age-restricted videos?**  
A: Some age-restricted content may require authentication. This feature is planned for future releases.

**Q: Can I use this on a server without display?**  
A: Yes, the tool works in headless environments. Progress bars will display properly in any terminal.

**Q: How many proxies can I test simultaneously?**  
A: Default is 10 concurrent threads. You can modify MAX_THREADS in the configuration.

**Q: Are premium/paid proxies supported?**  
A: Yes, use the format `username:password@ip:port` in your proxy.csv file.

---

## Support

For support and questions:

- **GitHub Issues**: [Report bugs or request features](https://github.com/zulfikriyahya/youtube-downloader/issues)
- **Discussions**: Join GitHub Discussions for community help
- **Email**: Contact via GitHub profile

---

## Changelog

### [4.0.0] - 2024

**Added**

- High-performance proxy system with concurrent testing
- Animated terminal UI with loading indicators
- Smart proxy selection and automatic fallback
- Real-time latency monitoring
- Enhanced progress bars with dynamic colors

**Changed**

- Optimized download performance with concurrent fragments
- Improved error handling and retry logic
- Better proxy validation and testing

**Fixed**

- Memory leaks in long-running downloads
- Progress bar accuracy issues
- Proxy timeout handling

---

## Security

### Reporting Vulnerabilities

If you discover a security vulnerability, please email the details to the project maintainer. Do not create public issues for security concerns.

### Best Practices

- Keep yt-dlp and dependencies updated
- Use trusted proxy sources only
- Avoid storing authentication credentials in plain text
- Review proxy.csv file permissions

**⭐ Star this repository if you find it useful!**
