import subprocess


def start_recording() -> subprocess.Popen:
    """launch ffmpeg as a background process"""
    # my camera is upside down so I flip the video
    CMD: str = (
        # "ffmpeg -f v4l2 -input_format mjpeg -video_size 1280x720 -i /dev/video0 -c:v libx264 -preset ultrafast -y flight.mp4"
        'ffmpeg -f v4l2 -input_format mjpeg -video_size 1280x720 -i /dev/video0 -c:v libx264 -preset ultrafast -vf "vflip,hflip" -y flight.mp4'
    )
    print("Recording started in background...")
    return subprocess.Popen(
        CMD,
        shell=True,
        stdin=subprocess.PIPE,
        start_new_session=True,
    )


def stop_recording(video_process: subprocess.Popen) -> None:
    """stops the recording and saves file"""
    video_process.communicate(input=b"q", timeout=10)
    return None


if __name__ == "__main__":
    video_proces: subprocess.Popen = start_recording()
    try:
        while True:
            __import__("time").sleep(1)
    except KeyboardInterrupt:
        stop_recording(video_proces)
        quit()
