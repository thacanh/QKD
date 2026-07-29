import os
import uvicorn
import gradio as gr
import spaces
from main import app as fastapi_app

# Top-level @spaces.GPU function for HF ZeroGPU runner
@spaces.GPU
def predict(text):
    return f"QuantumShield Backend Online: {text}"

# Create standard Gradio Interface with @spaces.GPU function
demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. API routes active at /api/health and /api/simulate",
)

# Mount FastAPI endpoints onto Gradio App
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
