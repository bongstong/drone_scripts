import subprocess
import os
import signal


def start_recording() -> subprocess.Popen:
    """--- START RECORDING ---
    launch FFmpeg as a background process"""
    # my camera is upside down so I flip the video
    CMD: str = (
        # "ffmpeg -f v4l2 -input_format mjpeg -video_size 1280x720 -i /dev/video0 -c:v libx264 -preset ultrafast -y flight.mp4"
        'ffmpeg -f v4l2 -input_format mjpeg -video_size 1280x720 -i /dev/video0 -c:v libx264 -preset ultrafast -vf "vflip,hflip" -y flight.mp4'
    )
    print("Recording started in background...")
    return subprocess.Popen(CMD, shell=True, preexec_fn=os.setsid)


def stop_recording(video_process: subprocess.Popen) -> None:
    """--- STOP RECORDING ---
    sends a 'Ctrl+C' signal to the background process to save the file"""
    os.killpg(os.getpgid(video_process.pid), signal.SIGINT)
    print("Recording stopped and saved.")
    return None


if __name__ == "__main__":
    video_proces: subprocess.Popen = start_recording()
    try:
        pass
    except KeyboardInterrupt:
        stop_recording(video_proces)
        quit()
