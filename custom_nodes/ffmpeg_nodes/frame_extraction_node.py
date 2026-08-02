from custom_nodes.shared.utils import get_logger
from custom_nodes.shared.pipeline_functions import extract_frames

logger = get_logger("frame_extraction_node")


class FrameExtractionNode:
    """Extracts frames from the validated video at a given fps."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"forceInput": True}),
                "output_dir": ("STRING", {"default": "/workspace/data/frames"}),
                "fps": ("INT", {"default": 2, "min": 1, "max": 10}),
            }
        }

    RETURN_TYPES = ("STRING",)  # outputs: frames directory
    RETURN_NAMES = ("frames_dir",)
    FUNCTION = "extract"
    CATEGORY = "3DGS Pipeline"

    def extract(self, video_path, output_dir, fps):
        result = extract_frames(video_path, output_dir, fps)
        logger.info(f"Frames extracted to: {result}")
        return (result,)


NODE_CLASS_MAPPINGS = {"FrameExtractionNode": FrameExtractionNode}
NODE_DISPLAY_NAME_MAPPINGS = {"FrameExtractionNode": "Frame Extraction (FFmpeg)"}