import os
import uvicorn
import gradio as gr
import spaces
from main import app as fastapi_app

# Define a ZeroGPU decorated function registered to Gradio event graph
@spaces.GPU
def check_gpu_status():
    return "ZeroGPU is active and ready!"

# Create Gradio Blocks interface registering the @spaces.GPU function
with gr.Blocks(title="QuantumShield FinEdu API") as demo:
    gr.Markdown("# 🛡️ QuantumShield FinEdu Backend API")
    gr.Markdown("Server Status: **Active & Ready**")
    gr.Markdown("API Endpoints: `/api/health` and `/api/simulate`")
    
    # Register the @spaces.GPU function on a Gradio button click event
    check_btn = gr.Button("Check GPU Status")
    status_out = gr.Textbox(label="Status")
    check_btn.click(fn=check_gpu_status, inputs=[], outputs=status_out)

# Mount FastAPI app onto Gradio
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
