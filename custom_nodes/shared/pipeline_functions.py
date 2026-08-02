"""
Core pipeline functions. Each ComfyUI node in this project is a thin
wrapper that calls one of these functions. Keeping logic here (instead
of inside each node file) avoids duplicating code across nodes.
"""

from pathlib import Path
from custom_nodes.shared.utils import get_logger, run_command, ensure_dir

logger = get_logger("pipeline")


def extract_frames(video_path: str, output_dir: str, fps: int = 2) -> str:
    """
    Extracts frames from a video using ffmpeg at a given rate (frames
    per second of video, not total frame count).

    fps=2 means: for every 1 second of video, save 2 frames. Lower fps
    means fewer, more spread-out frames (faster COLMAP, less detail).
    Higher fps means more frames (slower COLMAP, more detail/overlap).
    """
    ensure_dir(output_dir)
    output_pattern = str(Path(output_dir) / "frame_%05d.jpg")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-qscale:v", "2",  # high JPEG quality (2 = near-lossless, scale is 2-31)
        output_pattern,
    ]
    run_command(command, logger)
    return output_dir


def run_colmap(image_dir: str, workspace_dir: str) -> str:
    """
    Runs COLMAP's automatic reconstruction pipeline: feature extraction,
    matching, and sparse mapping, in one command. This is COLMAP's own
    convenience wrapper (colmap automatic_reconstructor) rather than us
    manually chaining feature_extractor -> matcher -> mapper ourselves.
    """
    ensure_dir(workspace_dir)

    command = [
        "colmap", "automatic_reconstructor",
        "--workspace_path", workspace_dir,
        "--image_path", image_dir,
        "--sparse", "1",
        "--dense", "0",  # we don't need dense reconstruction for 3DGS
    ]
    run_command(command, logger)

    sparse_dir = str(Path(workspace_dir) / "sparse" / "0")
    return sparse_dir


def train_gaussians(source_path: str, output_path: str, iterations: int = 7000) -> str:
    """
    Trains a 3D Gaussian Splatting scene using the official GraphDECO
    repo's train.py script. source_path must contain COLMAP's sparse
    reconstruction + the original images, in the folder layout GraphDECO
    expects (images/ and sparse/0/).

    iterations=7000 is GraphDECO's own "fast preview" checkpoint (their
    default full run is 30000). We use the lower number under time
    pressure - trades some quality for speed.
    """
    ensure_dir(output_path)

    command = [
        "python", "train.py",
        "-s", source_path,
        "-m", output_path,
        "--iterations", str(iterations),
    ]
    run_command(command, logger)
    return output_path


def export_scene(model_path: str) -> str:
    """
    GraphDECO's train.py already writes a point_cloud.ply file inside
    the model output directory during training - this function just
    locates it, rather than performing a separate export step.
    """
    ply_path = Path(model_path) / "point_cloud" / f"iteration_7000" / "point_cloud.ply"
    if not ply_path.exists():
        raise FileNotFoundError(f"Expected output not found: {ply_path}")
    return str(ply_path)