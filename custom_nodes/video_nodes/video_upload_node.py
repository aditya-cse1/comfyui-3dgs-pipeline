from custom_nodes.shared.utils import get_logger

logger = get_logger("video_upload_node")


class VideoUploadNode:
    """
    Takes a video file path and validates it exists. This is the
    entry point of the pipeline - every other node runs after this.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)  # outputs: validated video path
    RETURN_NAMES = ("video_path",)
    FUNCTION = "load_video"
    CATEGORY = "3DGS Pipeline"

    def load_video(self, video_path):
        import os
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        logger.info(f"Video validated: {video_path}")
        return (video_path,)


NODE_CLASS_MAPPINGS = {"VideoUploadNode": VideoUploadNode}
NODE_DISPLAY_NAME_MAPPINGS = {"VideoUploadNode": "Video Upload"}