import os
import uvicorn
import gradio as gr
from main import app as fastapi_app

# Create a simple Gradio status interface for HF Space homepage
demo = gr.Interface(
    fn=lambda: "🛡️ QuantumShield FinEdu Backend API is running smoothly!",
    inputs=[],
    outputs="text",
    title="QuantumShield FinEdu API Server",
    description="FastAPI Backend for QKD Simulation. Endpoints: /api/health and /api/simulate",
)

# Mount the FastAPI app onto Gradio
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
