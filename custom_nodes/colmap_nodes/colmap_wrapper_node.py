from custom_nodes.shared.utils import get_logger
from custom_nodes.shared.pipeline_functions import run_colmap

logger = get_logger("colmap_wrapper_node")


class ColmapWrapperNode:
    """Runs COLMAP's automatic reconstructor on extracted frames."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames_dir": ("STRING", {"forceInput": True}),
                "workspace_dir": ("STRING", {"default": "/workspace/data/colmap_out"}),
            }
        }

    RETURN_TYPES = ("STRING",)  # outputs: sparse reconstruction path (images + sparse/0)
    RETURN_NAMES = ("colmap_workspace",)
    FUNCTION = "run"
    CATEGORY = "3DGS Pipeline"

    def run(self, frames_dir, workspace_dir):
        run_colmap(frames_dir, workspace_dir)
        logger.info(f"COLMAP finished: {workspace_dir}")
        # GraphDECO expects the workspace root (contains images/ and sparse/0/),
        # not just the sparse/ subfolder - we return the workspace itself.
        return (workspace_dir,)


NODE_CLASS_MAPPINGS = {"ColmapWrapperNode": ColmapWrapperNode}
NODE_DISPLAY_NAME_MAPPINGS = {"ColmapWrapperNode": "COLMAP (SfM)"}