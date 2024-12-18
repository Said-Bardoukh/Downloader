import yt_dlp
import os
import ffmpeg


def download_from_youtube(url, filename, output_path=r'C:\Users\Admin\Desktop\Audio', media_type='video', quality='720p'):
    full_path = os.path.join(output_path, filename)

    # Enhanced compression settings
    video_format_code = {
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'best': 'bestvideo+bestaudio/best'
    }

    # Optimized base options
    ydl_opts = {
        'outtmpl': full_path + '.%(ext)s',
        'ignoreerrors': True,
        'noplaylist': True,
        'no_warnings': True,
        'continuedl': True,
        'quiet': False,
        'progress': True,
        'concurrent_fragments': 3  # Download multiple fragments at once
    }

    if media_type.lower() == 'video':
        ydl_opts.update({
            'format': video_format_code.get(quality, 'bestvideo+bestaudio/best'),
            'merge_output_format': 'mp4',
            # Enhanced video compression settings
            'postprocessor_args': [
                '-c:v', 'libx264',  # Use H.264 codec
                # Compression quality (23-28 is good balance)
                '-crf', '28',
                '-preset', 'faster',  # Faster encoding
                '-c:a', 'aac',      # Audio codec
                '-b:a', '128k'      # Reduced audio bitrate
            ]
        })
    else:  # audio
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality.replace('p', ''),
                'options': ['-compression_level', '8']  # Maximum compression
            }]
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nDownloading and compressing {
                  media_type} in {quality}...")
            ydl.download([url])

        extension = 'mp4' if media_type.lower() == 'video' else 'mp3'
        final_path = f"{full_path}.{extension}"

        # Additional compression after download for videos
        if media_type.lower() == 'video':
            compress_video(final_path)

        print(f"\n{media_type.capitalize()} downloaded and compressed successfully as: {
              filename}.{extension}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def compress_video(filepath):
    """Additional compression for video files"""
    temp_output = filepath + '.temp.mp4'
    try:
        # Use ffmpeg-python for additional compression
        stream = ffmpeg.input(filepath)
        stream = ffmpeg.output(stream, temp_output,
                               **{'c:v': 'libx264',
                                  'crf': '30',
                                  'preset': 'faster',
                                  'c:a': 'aac',
                                  'b:a': '96k'})
        ffmpeg.run(stream, overwrite_output=True,
                   capture_stdout=True, capture_stderr=True)

        # Replace original with compressed version
        os.replace(temp_output, filepath)
    except Exception as e:
        print(f"Additional compression failed: {e}")
        if os.path.exists(temp_output):
            os.remove(temp_output)


def get_user_input():
    # Get URL
    url = input("\nEnter YouTube URL: ")

    # Get custom filename
    filename = input("Enter the desired filename (without extension): ")

    # Get media type
    while True:
        media_type = input(
            "What do you want to download? (video/audio): ").lower()
        if media_type in ['video', 'audio']:
            break
        print("Please enter 'video' or 'audio'")

    # Get quality based on media type
    if media_type == 'video':
        while True:
            quality = input(
                "Choose quality (360p/480p/720p/1080p/best): ").lower()
            if quality in ['360p', '480p', '720p', '1080p', 'best']:
                break
            print("Please enter a valid quality option")
    else:  # audio
        while True:
            quality = input(
                "Choose audio quality (128p/192p/256p/320p): ").lower()
            if quality in ['128p', '192p', '256p', '320p']:
                break
            print("Please enter a valid audio quality option")

    return url, filename, media_type, quality


def main():
    print("\n=== YouTube Downloader ===")

    # Create output directory if it doesn't exist
    output_dir = r'C:\Users\Admin\Desktop\Audio'
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Get user inputs
        url, filename, media_type, quality = get_user_input()

        # Download the content
        download_from_youtube(url, filename, output_dir, media_type, quality)

        # Ask if user wants to download another
        while True:
            again = input(
                "\nDo you want to download another? (yes/no): ").lower()
            if again == 'yes':
                url, filename, media_type, quality = get_user_input()
                download_from_youtube(
                    url, filename, output_dir, media_type, quality)
            elif again == 'no':
                print("\nThank you for using the downloader!")
                break
            else:
                print("Please enter 'yes' or 'no'")

    except KeyboardInterrupt:
        print("\nDownload cancelled by user")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()