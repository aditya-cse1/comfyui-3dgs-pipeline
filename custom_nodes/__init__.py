from .video_nodes.video_upload_node import NODE_CLASS_MAPPINGS as m1, NODE_DISPLAY_NAME_MAPPINGS as d1
from .ffmpeg_nodes.frame_extraction_node import NODE_CLASS_MAPPINGS as m2, NODE_DISPLAY_NAME_MAPPINGS as d2
from .colmap_nodes.colmap_wrapper_node import NODE_CLASS_MAPPINGS as m3, NODE_DISPLAY_NAME_MAPPINGS as d3
from .gaussian_nodes.gaussian_train_node import NODE_CLASS_MAPPINGS as m4, NODE_DISPLAY_NAME_MAPPINGS as d4
from .viewer_nodes.export_viewer_node import NODE_CLASS_MAPPINGS as m5, NODE_DISPLAY_NAME_MAPPINGS as d5

NODE_CLASS_MAPPINGS = {**m1, **m2, **m3, **m4, **m5}
NODE_DISPLAY_NAME_MAPPINGS = {**d1, **d2, **d3, **d4, **d5}