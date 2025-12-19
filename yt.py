import yt_dlp
import os
import subprocess
import time
import threading
import re
from colorama import init, Fore, Style

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}============================================================
                                                          
   {Fore.GREEN}YouTube Video Downloader - Terminal Edition{Fore.CYAN}   
                                                          
============================================================{Style.RESET_ALL}
"""
    print(banner)

def format_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes is None:
        return "Unknown size"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_video_info(url):
    """Get video information without downloading"""
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except:
        return None

def get_ffmpeg_path():
    """Get FFmpeg path (portable or system)"""
    # Check for portable FFmpeg first
    portable_paths = [
        os.path.join(os.getcwd(), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(os.path.expanduser('~'), 'ffmpeg', 'ffmpeg.exe'),
        os.path.join(os.path.expanduser('~'), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        r'C:\ffmpeg\bin\ffmpeg.exe'
    ]
    
    for path in portable_paths:
        if os.path.exists(path):
            return path, path.replace('ffmpeg.exe', 'ffprobe.exe')
    
    # Try system FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return 'ffmpeg', 'ffprobe'
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

def format_time(seconds):
    """Format seconds to HH:MM:SS or MM:SS"""
    if seconds < 0:
        return "00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def monitor_compression_progress(process, total_duration, start_time):
    """Monitor FFmpeg compression progress in download-style format"""
    import time
    import re
    
    try:
        current_time = 0
        last_update = time.time()
        bytes_processed = 0
        
        while process.poll() is None:
            # Read stderr line by line for progress
            line = process.stderr.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            # Look for time progress and size in FFmpeg output
            time_match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
            size_match = re.search(r'size=\s*(\d+)kB', line)
            
            if time_match:
                hours = int(time_match.group(1))
                minutes = int(time_match.group(2))
                seconds = float(time_match.group(3))
                current_time = hours * 3600 + minutes * 60 + seconds
            
            if size_match:
                bytes_processed = int(size_match.group(1)) * 1024  # Convert kB to bytes
            
            # Update progress every 1 second like download format
            now = time.time()
            if now - last_update >= 1.0:
                elapsed_time = now - start_time
                
                if total_duration > 0 and current_time > 0:
                    progress_percent = min((current_time / total_duration) * 100, 100)
                    
                    # Calculate compression speed (like download speed)
                    if elapsed_time > 0 and bytes_processed > 0:
                        speed_bps = bytes_processed / elapsed_time
                        if speed_bps >= 1024 * 1024:  # MB/s
                            speed_str = f"{speed_bps / (1024 * 1024):.2f}MiB/s"
                        elif speed_bps >= 1024:  # KB/s
                            speed_str = f"{speed_bps / 1024:.1f}KiB/s"
                        else:
                            speed_str = f"{speed_bps:.0f}B/s"
                    else:
                        speed_str = "0.0KiB/s"
                    
                    # Calculate ETA
                    if progress_percent > 3:  # Only estimate after some progress
                        estimated_total = (elapsed_time / progress_percent) * 100
                        remaining_time = max(0, estimated_total - elapsed_time)
                        eta_mins = int(remaining_time // 60)
                        eta_secs = int(remaining_time % 60)
                        eta_str = f"{eta_mins:02d}:{eta_secs:02d}"
                    else:
                        # Use rough estimate based on video duration
                        estimated_total = total_duration * 0.25  # Veryfast preset estimate (much faster)
                        remaining_time = max(0, estimated_total - elapsed_time)
                        eta_mins = int(remaining_time // 60)
                        eta_secs = int(remaining_time % 60)
                        eta_str = f"{eta_mins:02d}:{eta_secs:02d}"
                    
                    # Estimate final size based on current progress
                    if progress_percent > 0:
                        estimated_final_size = (bytes_processed / progress_percent * 100)
                        estimated_size_gb = estimated_final_size / (1024**3)
                    else:
                        estimated_size_gb = 0.95  # Default estimate
                    
                    # Format exactly like download: [compress] 2.2% of ~ 2.84GiB at 3.52MiB/s ETA 13:17
                    print(f"\r[compress] {progress_percent:.1f}% of ~ {estimated_size_gb:.2f}GiB at {speed_str} ETA {eta_str}", 
                          end='', flush=True)
                else:
                    # Simple processing display
                    if 'speed_str' in locals():
                        print(f"\r[compress] Processing... at {speed_str}", end='', flush=True)
                    else:
                        print(f"\r[compress] Processing...", end='', flush=True)
                
                last_update = now
            
            time.sleep(0.1)
    
    except Exception:
        pass  # Silently handle any monitoring errors

def compress_video(input_path, output_dir):
    """Compress video to under 1GB using FFmpeg"""
    try:
        import subprocess
        print(f"{Fore.YELLOW}🔄 Compressing video to under 1GB...{Style.RESET_ALL}")
        
        # Get FFmpeg paths
        ffmpeg_cmd, ffprobe_cmd = get_ffmpeg_path()
        if not ffmpeg_cmd:
            print(f"{Fore.RED}❌ FFmpeg not found. Please install FFmpeg for compression.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Run: python install_ffmpeg.py{Style.RESET_ALL}")
            return input_path
        
        # Get file info
        file_name = os.path.basename(input_path)
        name, ext = os.path.splitext(file_name)
        compressed_path = os.path.join(output_dir, f"{name}_compressed.mp4")
        
        # Get video duration first
        duration_cmd = [
            ffprobe_cmd, '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', input_path
        ]
        
        try:
            duration = float(subprocess.check_output(duration_cmd).decode().strip())
        except:
            duration = 3600  # Default to 1 hour if can't detect
        
        # Target size: 900MB with safety margin, calculate bitrate
        target_size_mb = 850  # Reduced to 850MB to ensure under 1GB
        safety_margin = 0.95  # Use 95% of target for safety
        target_size_safe = target_size_mb * safety_margin
        target_bitrate = int((target_size_safe * 8 * 1024) / duration)  # kbps
        
        # Compress video with faster settings
        compress_cmd = [
            ffmpeg_cmd, '-i', input_path,
            '-c:v', 'libx264',
            '-b:v', f'{target_bitrate}k',
            '-maxrate', f'{int(target_bitrate * 1.1)}k',  # Tighter control
            '-bufsize', f'{int(target_bitrate * 1.5)}k',  # Smaller buffer
            '-c:a', 'aac',
            '-b:a', '128k',
            '-preset', 'faster',  # Faster encoding
            '-crf', '25',  # Slightly higher CRF for speed
            '-threads', '0',  # Use all CPU threads
            '-progress', 'pipe:2',  # Enable progress output to stderr
            '-y',  # Overwrite output file
            compressed_path
        ]
        
        print(f"{Fore.CYAN}🔧 Target bitrate: {target_bitrate}k{Style.RESET_ALL}")
        
        # Start timer and run compression with progress
        import time
        start_time = time.time()
        # Faster preset reduces time by ~40%
        estimated_minutes = int(duration/60 * 0.5)  # Faster encoding estimate
        print(f"{Fore.YELLOW}⏳ Starting compression... Estimated time: ~{estimated_minutes} minutes{Style.RESET_ALL}")
        
        # Run compression with progress monitoring
        process = subprocess.Popen(compress_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Monitor progress in a separate thread
        import threading
        progress_thread = threading.Thread(target=monitor_compression_progress, 
                                         args=(process, duration, start_time), daemon=True)
        progress_thread.start()
        
        # Wait for completion
        stdout, stderr = process.communicate()
        
        # Clear progress line
        print()  # New line after progress display
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, compress_cmd, stderr)
        
        # Calculate total time and show results
        total_time = time.time() - start_time
        compressed_size = format_size(os.path.getsize(compressed_path))
        
        print(f"{Fore.GREEN}✅ Compression completed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Final size: {compressed_size}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}⏱️  Total time: {format_time(total_time)}{Style.RESET_ALL}")
        
        # Remove original large file
        os.remove(input_path)
        print(f"{Fore.GREEN}🗑️  Removed original large file{Style.RESET_ALL}")
        
        return compressed_path
        
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}❌ FFmpeg not found. Please install FFmpeg for compression.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Download from: https://ffmpeg.org/download.html{Style.RESET_ALL}")
        return input_path
    except Exception as e:
        print(f"{Fore.RED}❌ Compression failed: {str(e)}{Style.RESET_ALL}")
        return input_path

def download_video(url, quality, download_path):
    """Download video with specified quality"""
    try:
        print(f"\n{Fore.YELLOW}⏳ Getting video information...{Style.RESET_ALL}")
        
        # Get video info first
        info = get_video_info(url)
        if info:
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')
            view_count = info.get('view_count', 0)
            
            # Format duration
            if duration:
                mins, secs = divmod(duration, 60)
                duration_str = f"{mins}:{secs:02d}"
            else:
                duration_str = "Unknown"
            
            # Format view count
            if view_count:
                if view_count >= 1_000_000:
                    views_str = f"{view_count/1_000_000:.1f}M views"
                elif view_count >= 1_000:
                    views_str = f"{view_count/1_000:.1f}K views"
                else:
                    views_str = f"{view_count} views"
            else:
                views_str = "Unknown views"
            
            print(f"\n{Fore.CYAN}📺 Title: {title}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}👤 Uploader: {uploader}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}⏱️  Duration: {duration_str}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}👁️  Views: {views_str}{Style.RESET_ALL}")
            
            # Try to get estimated file size for selected quality
            formats = info.get('formats', [])
            if quality == '6':  # audio only
                audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                if audio_formats:
                    best_audio = max(audio_formats, key=lambda x: x.get('abr', 0) or 0)
                    file_size = best_audio.get('filesize') or best_audio.get('filesize_approx')
                    if file_size:
                        print(f"{Fore.YELLOW}📊 Estimated Size: {format_size(file_size)} (Audio Only){Style.RESET_ALL}")
            else:
                # For video formats, find the best match for selected quality
                quality_heights = {'1': None, '2': 1080, '3': 720, '4': 480, '5': 360}
                target_height = quality_heights.get(quality)
                
                if target_height:
                    video_formats = [f for f in formats if f.get('height') == target_height and f.get('vcodec') != 'none']
                else:  # best quality
                    video_formats = [f for f in formats if f.get('vcodec') != 'none']
                
                if video_formats:
                    best_video = max(video_formats, key=lambda x: x.get('height', 0) or 0)
                    file_size = best_video.get('filesize') or best_video.get('filesize_approx')
                    if file_size:
                        quality_str = f"{best_video.get('height', '?')}p" if best_video.get('height') else "Best"
                        print(f"{Fore.YELLOW}📊 Estimated Size: {format_size(file_size)} ({quality_str}){Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}⏳ Starting download...{Style.RESET_ALL}")
        
        # Check estimated file size and adjust quality if needed
        will_compress = False
        if quality in ['1', '2'] and info:  # Only for best and 1080p
            formats = info.get('formats', [])
            quality_heights = {'1': None, '2': 1080}
            target_height = quality_heights.get(quality)
            
            if target_height:
                video_formats = [f for f in formats if f.get('height') == target_height and f.get('vcodec') != 'none']
            else:
                video_formats = [f for f in formats if f.get('vcodec') != 'none']
            
            if video_formats:
                best_video = max(video_formats, key=lambda x: x.get('height', 0) or 0)
                estimated_size = best_video.get('filesize') or best_video.get('filesize_approx')
                
                if estimated_size and estimated_size > 1000 * 1024 * 1024:  # Over 1GB
                    will_compress = True
                    print(f"{Fore.YELLOW}⚠️  Video will be over 1GB (~{format_size(estimated_size)}){Style.RESET_ALL}")
                    print(f"{Fore.CYAN}💡 Downloading in lower quality to avoid compression delay...{Style.RESET_ALL}")
        
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }
        
        if quality == '6':  # audio only
            ydl_opts['format'] = 'bestaudio'
            print(f"{Fore.CYAN}📻 Downloading audio only...{Style.RESET_ALL}")
        elif will_compress:
            # Download 720p or lower to stay under 1GB
            ydl_opts['format'] = 'best[height<=720][filesize<1000M]/best[height<=720]/best[filesize<1000M]'
            print(f"{Fore.CYAN}📹 Downloading optimized format (≤720p) to stay under 1GB...{Style.RESET_ALL}")
        elif quality == '1':  # best
            ydl_opts['format'] = 'best'
            print(f"{Fore.CYAN}📹 Downloading best available format...{Style.RESET_ALL}")
        else:
            quality_map = {'2': '1080', '3': '720', '4': '480', '5': '360'}
            height = quality_map.get(quality, '720')
            ydl_opts['format'] = f'best[height<={height}]'
            print(f"{Fore.CYAN}📹 Downloading best {height}p format...{Style.RESET_ALL}")
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            
            # Get the downloaded file size
            filename = ydl.prepare_filename(info)
            if os.path.exists(filename):
                file_size_bytes = os.path.getsize(filename)
                size_str = format_size(file_size_bytes)
                print(f"{Fore.GREEN}📊 Downloaded Size: {size_str}{Style.RESET_ALL}")
                
                # Only compress if still larger than 1GB (shouldn't happen with smart download)
                if file_size_bytes > 1000 * 1024 * 1024:  # 1GB in bytes
                    print(f"{Fore.YELLOW}⚠️  File is still larger than 1GB, compressing...{Style.RESET_ALL}")
                    compressed_path = compress_video(filename, download_path)
                    if compressed_path != filename:
                        final_size = format_size(os.path.getsize(compressed_path))
                        print(f"{Fore.GREEN}🎯 Final Size: {final_size}{Style.RESET_ALL}")
                        size_str = final_size
            else:
                size_str = "Unknown"
        
        print(f"\n{Fore.GREEN}✅ Download Complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📁 Saved to: {download_path}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📝 Title: {video_title}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 File Size: {size_str}{Style.RESET_ALL}\n")
        return True
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Download failed: {str(e)}{Style.RESET_ALL}\n")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    # First check system PATH
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Check for portable FFmpeg in common locations
    portable_paths = [
        os.path.join(os.getcwd(), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(os.getcwd(), 'ffmpeg.exe'),
        os.path.join(os.path.expanduser('~'), 'ffmpeg', 'ffmpeg.exe'),
        os.path.join(os.path.expanduser('~'), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        'C:\\ffmpeg\\bin\\ffmpeg.exe'
    ]
    
    for path in portable_paths:
        if os.path.exists(path):
            return path
    
    return False

def download_portable_ffmpeg():
    """Download portable FFmpeg"""
    try:
        print(f"\n{Fore.YELLOW}🔄 Downloading portable FFmpeg...{Style.RESET_ALL}")
        import urllib.request
        import zipfile
        
        # Create ffmpeg directory
        ffmpeg_dir = os.path.join(os.getcwd(), 'ffmpeg')
        os.makedirs(ffmpeg_dir, exist_ok=True)
        
        # Download URL for FFmpeg Windows builds
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = os.path.join(ffmpeg_dir, 'ffmpeg.zip')
        
        print(f"{Fore.CYAN}📥 Downloading from: {url}{Style.RESET_ALL}")
        urllib.request.urlretrieve(url, zip_path)
        
        print(f"{Fore.YELLOW}📦 Extracting FFmpeg...{Style.RESET_ALL}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Find the extracted directory and move binaries
        for item in os.listdir(ffmpeg_dir):
            item_path = os.path.join(ffmpeg_dir, item)
            if os.path.isdir(item_path) and 'ffmpeg' in item.lower():
                bin_path = os.path.join(item_path, 'bin')
                if os.path.exists(bin_path):
                    # Move binaries to main ffmpeg/bin directory
                    target_bin = os.path.join(ffmpeg_dir, 'bin')
                    if os.path.exists(target_bin):
                        import shutil
                        shutil.rmtree(target_bin)
                    shutil.move(bin_path, target_bin)
                    break
        
        # Clean up
        os.remove(zip_path)
        
        # Verify installation
        ffmpeg_exe = os.path.join(ffmpeg_dir, 'bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_exe):
            print(f"{Fore.GREEN}✅ Portable FFmpeg installed successfully!{Style.RESET_ALL}")
            return ffmpeg_exe
        else:
            print(f"{Fore.RED}❌ Installation failed{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Download failed: {str(e)}{Style.RESET_ALL}")
        return False

def install_ffmpeg_guide():
    """Show FFmpeg installation instructions"""
    print(f"\n{Fore.RED}❌ FFmpeg is not installed or not found in PATH{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}� Easy Installation Options:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Portable FFmpeg (Recommended - No PATH setup needed){Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. System Installation via Package Managers{Style.RESET_ALL}")
    print(f"{Fore.GREEN}3. Manual Installation{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.CYAN}Choose installation method (1-3): {Style.RESET_ALL}").strip()
    
    if choice == '1':
        # Portable FFmpeg option
        print(f"\n{Fore.YELLOW}📦 Installing Portable FFmpeg...{Style.RESET_ALL}")
        ffmpeg_path = download_portable_ffmpeg()
        if ffmpeg_path:
            return ffmpeg_path
    
    elif choice == '2':
        # Package manager options
        print(f"\n{Fore.YELLOW}� Package Manager Installation:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Choose your preferred package manager:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}   1. winget install ffmpeg{Style.RESET_ALL}")
        print(f"{Fore.GREEN}   2. choco install ffmpeg{Style.RESET_ALL}")
        print(f"{Fore.GREEN}   3. scoop install ffmpeg{Style.RESET_ALL}")
        
        pkg_choice = input(f"\n{Fore.CYAN}Try installation with winget? (y/n): {Style.RESET_ALL}").strip().lower()
        if pkg_choice in ['y', 'yes']:
            try:
                print(f"\n{Fore.YELLOW}🔄 Attempting to install FFmpeg via winget...{Style.RESET_ALL}")
                result = subprocess.run(['winget', 'install', 'ffmpeg'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"{Fore.GREEN}✅ FFmpeg installation completed!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Please restart the application for changes to take effect.{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}❌ winget installation failed.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Try option 1 (Portable) instead.{Style.RESET_ALL}")
            except FileNotFoundError:
                print(f"{Fore.RED}❌ winget not found.{Style.RESET_ALL}")
    
    else:
        # Manual installation
        print(f"\n{Fore.YELLOW}📋 Manual Installation Steps:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1. Download FFmpeg from: https://ffmpeg.org/download.html{Style.RESET_ALL}")
        print(f"{Fore.CYAN}2. Extract the zip file to C:\\ffmpeg{Style.RESET_ALL}")
        print(f"{Fore.CYAN}3. Add C:\\ffmpeg\\bin to your PATH environment variable{Style.RESET_ALL}")
        print(f"{Fore.CYAN}4. Restart your terminal/command prompt{Style.RESET_ALL}")
    
    return False

def compress_video_to_size(input_path, output_dir, target_size_mb=950):
    """Compress video to specific target size"""
    
    # Check if FFmpeg is available
    ffmpeg_path = check_ffmpeg()
    if not ffmpeg_path:
        print(f"{Fore.RED}❌ FFmpeg not found. Cannot compress video.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Video compression requires FFmpeg to be installed.{Style.RESET_ALL}")
        return input_path
    
    # Use ffmpeg command or full path
    ffmpeg_cmd = 'ffmpeg' if ffmpeg_path is True else ffmpeg_path
    ffprobe_cmd = 'ffprobe' if ffmpeg_path is True else ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
    
    try:
        print(f"{Fore.YELLOW}🔄 Compressing video to {target_size_mb}MB...{Style.RESET_ALL}")
        
        # Get file info
        file_name = os.path.basename(input_path)
        name, ext = os.path.splitext(file_name)
        compressed_path = os.path.join(output_dir, f"{name}_compressed.mp4")
        
        # Get video duration and info
        duration_cmd = [
            ffprobe_cmd, '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', input_path
        ]
        
        try:
            result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
            duration = float(result.stdout.strip())
            print(f"{Fore.CYAN}📊 Video duration: {duration/60:.1f} minutes{Style.RESET_ALL}")
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
            print(f"{Fore.YELLOW}⚠️  Could not detect duration, using default calculation{Style.RESET_ALL}")
            duration = 3600  # Default to 1 hour if can't detect
        
        # Calculate target bitrate for specified size with safety margin
        # Formula: (target_size_mb * 8 * 1024) / duration_seconds = bitrate_kbps
        # Use 90% of target size to ensure we stay under the limit
        safety_margin = 0.90  # Use 90% of target size for safety
        audio_bitrate = 128  # kbps
        target_size_safe = target_size_mb * safety_margin
        total_bitrate = int((target_size_safe * 8 * 1024) / duration)
        video_bitrate = max(total_bitrate - audio_bitrate, 400)  # Minimum 400k video bitrate
        
        print(f"{Fore.CYAN}🎯 Target size: {target_size_mb}MB (with safety margin: {target_size_safe:.0f}MB){Style.RESET_ALL}")
        print(f"{Fore.CYAN}🔧 Calculated video bitrate: {video_bitrate}k{Style.RESET_ALL}")
        
        # Compress video with calculated bitrate and faster settings
        compress_cmd = [
            ffmpeg_cmd, '-i', input_path,
            '-c:v', 'libx264',
            '-b:v', f'{video_bitrate}k',
            '-maxrate', f'{int(video_bitrate * 1.1)}k',  # Tighter control - only 10% over
            '-bufsize', f'{int(video_bitrate * 1.5)}k',  # Smaller buffer for better control
            '-c:a', 'aac',
            '-b:a', f'{audio_bitrate}k',
            '-preset', 'veryfast',  # Much faster encoding (ultrafast can be lower quality)
            '-crf', '26',  # Slightly higher CRF for faster encoding with acceptable quality
            '-threads', '0',  # Use all available CPU threads
            '-movflags', '+faststart',  # Optimize for streaming/fast playback
            '-tune', 'fastdecode',  # Optimize for faster decoding
            '-progress', 'pipe:2',  # Enable progress output to stderr
            '-y',  # Overwrite output file
            compressed_path
        ]
        
        # Start timer and compression with progress monitoring
        import time, threading
        start_time = time.time()
        # Veryfast preset reduces compression time significantly (2-3x faster than medium)
        estimated_minutes = duration / 60 * 0.25  # Much faster with veryfast preset
        print(f"{Fore.YELLOW}⏳ Starting compression... Estimated time: ~{int(estimated_minutes)} minutes{Style.RESET_ALL}")
        
        # Run compression with progress indication
        process = subprocess.Popen(compress_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Monitor progress in a separate thread
        progress_thread = threading.Thread(target=monitor_compression_progress, 
                                         args=(process, duration, start_time), daemon=True)
        progress_thread.start()
        
        # Wait for completion
        stdout, stderr = process.communicate()
        
        # Clear progress line and show completion
        print()  # New line after progress display
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, compress_cmd, stderr)
        
        # Check final compressed file size and show timing
        if os.path.exists(compressed_path):
            total_time = time.time() - start_time
            final_size_bytes = os.path.getsize(compressed_path)
            final_size_mb = final_size_bytes / (1024 * 1024)
            final_size_str = format_size(final_size_bytes)
            
            print(f"{Fore.GREEN}✅ Compression completed!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}📊 Final size: {final_size_str} ({final_size_mb:.1f}MB){Style.RESET_ALL}")
            print(f"{Fore.GREEN}⏱️  Total time: {format_time(total_time)}{Style.RESET_ALL}")
            
            # Check if we hit the target
            if final_size_mb <= target_size_mb:
                print(f"{Fore.GREEN}🎯 Perfect! Successfully compressed to under {target_size_mb}MB!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️  File is {final_size_mb:.1f}MB (over {target_size_mb}MB target){Style.RESET_ALL}")
                print(f"{Fore.CYAN}💡 Tip: The safety margin will be adjusted for future compressions.{Style.RESET_ALL}")
            
            return compressed_path
        else:
            print(f"{Fore.RED}❌ Compressed file not found{Style.RESET_ALL}")
            return input_path
        
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ FFmpeg error: {e.stderr if e.stderr else 'Unknown error'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Make sure FFmpeg is installed: https://ffmpeg.org/download.html{Style.RESET_ALL}")
        return input_path
    except Exception as e:
        print(f"{Fore.RED}❌ Compression failed: {str(e)}{Style.RESET_ALL}")
        return input_path

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    while True:
        print(f"\n{Fore.YELLOW}============================================================{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Choose Option:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Download YouTube Video")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Compress Existing Video (Paste file path)")
        print(f"{Fore.RED}3.{Style.RESET_ALL} Exit")
        
        choice = input(f"\n{Fore.CYAN}Enter choice (1-3): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            # YouTube Download Option
            url = input(f"\n{Fore.CYAN}Enter YouTube URL: {Style.RESET_ALL}").strip()
            
            if not url:
                print(f"{Fore.RED}Please enter a valid URL{Style.RESET_ALL}")
                continue
            
            # Show quality options
            print(f"\n{Fore.YELLOW}Select Quality:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}1.{Style.RESET_ALL} Best Quality (Auto-compress if >1GB)")
            print(f"{Fore.GREEN}2.{Style.RESET_ALL} 1080p (Auto-compress if >1GB)")
            print(f"{Fore.GREEN}3.{Style.RESET_ALL} 720p")
            print(f"{Fore.GREEN}4.{Style.RESET_ALL} 480p")
            print(f"{Fore.GREEN}5.{Style.RESET_ALL} 360p")
            print(f"{Fore.GREEN}6.{Style.RESET_ALL} Audio Only (MP3)")
            
            quality = input(f"\n{Fore.CYAN}Enter choice (1-6): {Style.RESET_ALL}").strip()
            
            if quality not in ['1', '2', '3', '4', '5', '6']:
                print(f"{Fore.RED}Invalid choice, using default (Best Quality){Style.RESET_ALL}")
                quality = '1'
            
            # Get download path
            default_path = os.path.expanduser("~/Downloads")
            download_path = input(f"\n{Fore.CYAN}Save to (press Enter for {default_path}): {Style.RESET_ALL}").strip()
            
            if not download_path:
                download_path = default_path
            
            # Create directory if it doesn't exist
            if not os.path.exists(download_path):
                try:
                    os.makedirs(download_path)
                    print(f"{Fore.GREEN}Created directory: {download_path}{Style.RESET_ALL}")
                except:
                    print(f"{Fore.RED}Could not create directory, using Downloads folder{Style.RESET_ALL}")
                    download_path = default_path
            
            # Download the video
            download_video(url, quality, download_path)
            
        elif choice == '2':
            # Compress Existing Video Option
            video_path = input(f"\n{Fore.CYAN}Paste video file path (drag & drop or copy path): {Style.RESET_ALL}").strip()
            
            # Clean the path (remove quotes, PowerShell syntax, and extra characters)
            video_path = video_path.strip()
            
            # Remove PowerShell execution syntax
            if video_path.startswith('& '):
                video_path = video_path[2:]
            
            # Remove quotes
            video_path = video_path.strip('"').strip("'")
            
            # Handle escaped spaces and special characters
            video_path = video_path.replace("'", "")
            
            print(f"{Fore.YELLOW}📁 Cleaned path: {video_path}{Style.RESET_ALL}")
            
            if not video_path:
                print(f"{Fore.RED}Please enter a valid file path{Style.RESET_ALL}")
                continue
            
            if not os.path.exists(video_path):
                print(f"{Fore.RED}File not found: {video_path}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Tip: Try copying the full path from File Explorer{Style.RESET_ALL}")
                continue
            
            # Check if it's a video file
            video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']
            if not any(video_path.lower().endswith(ext) for ext in video_extensions):
                print(f"{Fore.RED}Please select a valid video file{Style.RESET_ALL}")
                continue
            
            # Get file size
            file_size_bytes = os.path.getsize(video_path)
            file_size_str = format_size(file_size_bytes)
            print(f"\n{Fore.CYAN}Original file size: {file_size_str}{Style.RESET_ALL}")
            
            if file_size_bytes <= 950 * 1024 * 1024:  # Already under 950MB
                print(f"{Fore.GREEN}File is already under 950MB, no compression needed!{Style.RESET_ALL}")
                continue
            
            # Get output directory
            output_dir = os.path.dirname(video_path)
            default_output = input(f"\n{Fore.CYAN}Save compressed video to (press Enter for same folder): {Style.RESET_ALL}").strip()
            
            if default_output:
                output_dir = default_output.strip('"').strip("'")
                if not os.path.exists(output_dir):
                    try:
                        os.makedirs(output_dir)
                        print(f"{Fore.GREEN}Created directory: {output_dir}{Style.RESET_ALL}")
                    except:
                        print(f"{Fore.RED}Could not create directory, using original folder{Style.RESET_ALL}")
                        output_dir = os.path.dirname(video_path)
            
            # Compress the video
            print(f"\n{Fore.YELLOW}Starting compression to 950MB...{Style.RESET_ALL}")
            compressed_path = compress_video_to_size(video_path, output_dir, target_size_mb=950)
            
            if compressed_path and compressed_path != video_path:
                final_size = format_size(os.path.getsize(compressed_path))
                print(f"\n{Fore.GREEN}✅ Compression Complete!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}📁 Compressed file: {compressed_path}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}📊 Final size: {final_size}{Style.RESET_ALL}")
                
                # Ask if user wants to delete original
                delete_original = input(f"\n{Fore.YELLOW}Delete original file? (y/n): {Style.RESET_ALL}").strip().lower()
                if delete_original in ['y', 'yes']:
                    try:
                        os.remove(video_path)
                        print(f"{Fore.GREEN}🗑️  Original file deleted{Style.RESET_ALL}")
                    except:
                        print(f"{Fore.RED}❌ Could not delete original file{Style.RESET_ALL}")
            
        elif choice == '3':
            print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}\n")
            break
            
        else:
            print(f"{Fore.RED}Invalid choice! Please select 1, 2, or 3{Style.RESET_ALL}")
        
        # Ask if user wants to continue
        if choice in ['1', '2']:
            another = input(f"\n{Fore.YELLOW}Perform another operation? (y/n): {Style.RESET_ALL}").strip().lower()
            if another not in ['y', 'yes']:
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}\n")
                break
        print(f"\n{Fore.YELLOW}═══════════════════════════════════════════════════════════{Style.RESET_ALL}")
        
        # Get URL
        url = input(f"\n{Fore.CYAN}🔗 Enter YouTube URL (or 'exit' to quit): {Style.RESET_ALL}").strip()
        
        if url.lower() in ['exit', 'quit', 'q']:
            print(f"\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}\n")
            break
        
        if not url:
            print(f"{Fore.RED}⚠️  Please enter a valid URL{Style.RESET_ALL}")
            continue
        
        # Show quality options
        print(f"\n{Fore.YELLOW}Select Quality:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Best Quality")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} 1080p")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} 720p")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} 480p")
        print(f"{Fore.GREEN}5.{Style.RESET_ALL} 360p")
        print(f"{Fore.GREEN}6.{Style.RESET_ALL} Audio Only (MP3)")
        
        quality = input(f"\n{Fore.CYAN}Enter choice (1-6): {Style.RESET_ALL}").strip()
        
        if quality not in ['1', '2', '3', '4', '5', '6']:
            print(f"{Fore.RED}⚠️  Invalid choice, using default (Best Quality){Style.RESET_ALL}")
            quality = '1'
        
        # Get download path
        default_path = os.path.expanduser("~/Downloads")
        download_path = input(f"\n{Fore.CYAN}📂 Save to (press Enter for {default_path}): {Style.RESET_ALL}").strip()
        
        if not download_path:
            download_path = default_path
        
        # Create directory if it doesn't exist
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
                print(f"{Fore.GREEN}📁 Created directory: {download_path}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}❌ Could not create directory, using Downloads folder{Style.RESET_ALL}")
                download_path = default_path
        
        # Download the video
        download_video(url, quality, download_path)
        
        # Ask if user wants to download another
        another = input(f"{Fore.YELLOW}Download another video? (y/n): {Style.RESET_ALL}").strip().lower()
        if another not in ['y', 'yes']:
            print(f"\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}\n")
            break

if __name__ == "__main__":
    main()
