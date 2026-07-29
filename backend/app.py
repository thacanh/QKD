import uvicorn
import gradio as gr
import spaces
from main import app as fastapi_app

# Top-level @spaces.GPU function for HF ZeroGPU launcher
@spaces.GPU
def predict_gpu(text: str):
    return f"QuantumShield ZeroGPU Online: {text}"

# Standard Gradio Interface registering @spaces.GPU function
demo = gr.Interface(
    fn=predict_gpu,
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /v1/simulate, /api/simulate, /simulate",
)

# Mount Gradio UI onto main FastAPI app
# fastapi_app natively handles /v1/simulate, /api/simulate, /simulate, /v1/health, /api/health, /health
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
