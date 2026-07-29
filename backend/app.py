import os
import uvicorn
import gradio as gr
from main import app as fastapi_app

# Add dummy @spaces.GPU function to satisfy Hugging Face ZeroGPU runner
try:
    import spaces
    @spaces.GPU
    def gpu_check():
        return "GPU Ready"
except Exception:
    pass

# Create a lightweight Gradio interface so HF Space detects the app
with gr.Blocks(title="QuantumShield FinEdu API") as demo:
    gr.Markdown("# 🛡️ QuantumShield FinEdu Backend API")
    gr.Markdown("Server is running! API Endpoints: `/api/health` and `/api/simulate`")

# Mount FastAPI app onto Gradio
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
