from pathlib import Path
from custom_nodes.shared.utils import get_logger

logger = get_logger("export_viewer_node")


class ExportViewerNode:
    """
    Locates the trained Gaussian scene's .ply file, ready for
    SuperSplat viewing. Takes the exact iteration count used in
    training, so it always finds the correct checkpoint folder.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {"forceInput": True}),
                "iterations": ("INT", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ply_path",)
    FUNCTION = "locate"
    CATEGORY = "3DGS Pipeline"

    def locate(self, model_path, iterations):
        ply_path = Path(model_path) / "point_cloud" / f"iteration_{iterations}" / "point_cloud.ply"
        if not ply_path.exists():
            raise FileNotFoundError(f"Expected output not found: {ply_path}")
        logger.info(f"Scene ready for SuperSplat: {ply_path}")
        return (str(ply_path),)


NODE_CLASS_MAPPINGS = {"ExportViewerNode": ExportViewerNode}
NODE_DISPLAY_NAME_MAPPINGS = {"ExportViewerNode": "Export for SuperSplat"}