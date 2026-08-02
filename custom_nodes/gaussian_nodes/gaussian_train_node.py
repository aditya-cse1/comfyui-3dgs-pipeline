from custom_nodes.shared.utils import get_logger
from custom_nodes.shared.pipeline_functions import train_gaussians

logger = get_logger("gaussian_train_node")


class GaussianTrainNode:
    """Trains a 3D Gaussian Splatting scene using official GraphDECO code."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "colmap_workspace": ("STRING", {"forceInput": True}),
                "output_dir": ("STRING", {"default": "/workspace/data/gaussian_output"}),
                "iterations": ("INT", {"default": 7000, "min": 1000, "max": 30000}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")  # model path, iterations used
    RETURN_NAMES = ("model_path", "iterations")
    FUNCTION = "train"
    CATEGORY = "3DGS Pipeline"

    def train(self, colmap_workspace, output_dir, iterations):
        result = train_gaussians(colmap_workspace, output_dir, iterations)
        logger.info(f"Training complete: {result}")
        return (result, iterations)


NODE_CLASS_MAPPINGS = {"GaussianTrainNode": GaussianTrainNode}
NODE_DISPLAY_NAME_MAPPINGS = {"GaussianTrainNode": "3D Gaussian Splatting Training"}