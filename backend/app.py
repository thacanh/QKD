import gradio as gr
import spaces
from main import app as fastapi_app

# Top-level @spaces.GPU function for HF ZeroGPU runner
@spaces.GPU
def predict(text):
    return f"QuantumShield Backend Online: {text}"

# Create standard Gradio Interface for HF Space
demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. Endpoints active at /api/health and /api/simulate",
)

# Attach FastAPI router directly onto Gradio's internal FastAPI application
demo.app.include_router(fastapi_app.router)
