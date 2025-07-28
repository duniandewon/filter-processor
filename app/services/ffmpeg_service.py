import subprocess
import tempfile


def apply_lut_with_ffmpeg(input_bytes: bytes, cube_file_path: str) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".jpg") as input_file, tempfile.NamedTemporaryFile(suffix=".jpg") as output_file:
        input_file.write(input_bytes)
        input_file.flush()

        result = subprocess.run([
            "ffmpeg",
            "-y",  # Overwrite output if exists
            "-i", input_file.name,
            "-vf", f"lut3d={cube_file_path}",
            output_file.name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print("FFmpeg error:", result.stderr.decode())
            raise RuntimeError("FFmpeg failed to apply LUT")

        output_file.seek(0)
        return output_file.read()
