import os
from pathlib import Path
from custom_nodes.shared.utils import get_logger, run_command, ensure_dir

logger = get_logger("pipeline")


def extract_frames(video_path: str, output_dir: str, fps: int = 3) -> str:
    ensure_dir(output_dir)
    output_pattern = str(Path(output_dir) / "frame_%05d.jpg")
    command = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps}",
        "-qscale:v", "2",
        output_pattern,
    ]
    run_command(command, logger)
    return output_dir


def run_colmap(image_dir: str, workspace_dir: str) -> str:
    ensure_dir(workspace_dir)
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    command = [
        "colmap", "automatic_reconstructor",
        "--workspace_path", workspace_dir,
        "--image_path", image_dir,
        "--sparse", "1",
        "--dense", "0",
    ]
    run_command(command, logger)

    sparse_dir = Path(workspace_dir) / "sparse" / "0"
    if not sparse_dir.exists():
        raise RuntimeError(f"COLMAP did not produce expected sparse/0 folder: {sparse_dir}")
    return str(sparse_dir)


def undistort_images(image_dir: str, colmap_sparse_dir: str, output_dir: str) -> str:
    """
    GraphDECO's train.py only accepts undistorted camera models
    (PINHOLE / SIMPLE_PINHOLE). COLMAP's automatic_reconstructor
    produces SIMPLE_RADIAL by default, so this step is required
    before training.
    """
    ensure_dir(output_dir)
    input_sparse_root = str(Path(colmap_sparse_dir).parent)  # sparse/ (contains 0/)

    command = [
        "colmap", "image_undistorter",
        "--image_path", image_dir,
        "--input_path", colmap_sparse_dir,
        "--output_path", output_dir,
        "--output_type", "COLMAP",
    ]
    run_command(command, logger)

    # image_undistorter writes sparse/ directly (not sparse/0/) - normalize it
    sparse_out = Path(output_dir) / "sparse"
    sparse_0 = sparse_out / "0"
    if not sparse_0.exists():
        ensure_dir(str(sparse_0))
        for f in sparse_out.glob("*.bin"):
            f.rename(sparse_0 / f.name)
        for f in sparse_out.glob("*.txt"):
            f.rename(sparse_0 / f.name)

    return output_dir


def train_gaussians(source_path: str, output_path: str, iterations: int = 7000) -> str:
    ensure_dir(output_path)
    gs_repo = "/workspace/comfyui-3dgs-pipeline/gaussian-splatting"
    command = [
        "python3", f"{gs_repo}/train.py",
        "-s", source_path,
        "-m", output_path,
        "--iterations", str(iterations),
    ]
    run_command(command, logger)
    return output_path


def export_scene(model_path: str, iterations: int = 7000) -> str:
    ply_path = Path(model_path) / "point_cloud" / f"iteration_{iterations}" / "point_cloud.ply"
    if not ply_path.exists():
        raise FileNotFoundError(f"Expected output not found: {ply_path}")
    return str(ply_path)
