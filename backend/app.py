import os
import uvicorn
import gradio as gr
from main import app as fastapi_app

# ZeroGPU compatibility handler for Hugging Face Spaces
try:
    import spaces

    @spaces.GPU(duration=1)
    def dummy_gpu_task():
        return "GPU active"

    try:
        dummy_gpu_task()
    except Exception:
        pass
except Exception:
    pass

# Create a lightweight Gradio UI for HF Space
with gr.Blocks(title="QuantumShield FinEdu API") as demo:
    gr.Markdown("# 🛡️ QuantumShield FinEdu Backend API")
    gr.Markdown("Server status: **Active & Ready**")
    gr.Markdown("API Endpoints: `/api/health` and `/api/simulate`")

# Mount FastAPI app onto Gradio
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
