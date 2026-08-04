import gradio as gr

PLY_PATH = "/workspace/comfyui-3dgs-pipeline/data/gaussian_output/point_cloud/iteration_7000/point_cloud.ply"

def show_result():
    return PLY_PATH, "Training complete — 26 images registered, 7000 iterations, PSNR 31.1"

with gr.Blocks(title="Video to 3D Gaussian Splatting") as demo:
    gr.Markdown("# Video → 3D Gaussian Splatting Pipeline")
    gr.Markdown("Pipeline: Frame Extraction → COLMAP (SfM) → 3D Gaussian Training → Export")
    btn = gr.Button("Show Trained Scene Result")
    output_file = gr.File(label="Download .ply (view in SuperSplat)")
    status = gr.Textbox(label="Status")
    btn.click(fn=show_result, outputs=[output_file, status])

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
