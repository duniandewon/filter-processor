import subprocess
import tempfile


def apply_lut_with_ffmpeg(input_bytes: bytes, cube_file_path: str) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".jpg") as input_file, tempfile.NamedTemporaryFile(suffix=".jpg") as output_file:
        input_file.write(input_bytes)
        input_file.flush()

        cmd = [
            "ffmpeg",
            "-y",
            "-i", "pipe:0",
            "-vf", f"lut3d={cube_file_path}",
            "-f", "image2",
            "-vcodec", "mjpeg",
            "pipe:1"
        ]

        proc = subprocess.run(
            cmd,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    if proc.returncode != 0:
        print(proc.stderr.decode())
        raise RuntimeError("ffmpeg error")

    return proc.stdout
