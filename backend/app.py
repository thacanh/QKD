import gradio as gr
from main import app as fastapi_app

# Create a lightweight Gradio interface for HF Space
demo = gr.Interface(
    fn=lambda text: f"QuantumShield Backend Online: {text}",
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /api/health and /api/simulate",
)

# Mount FastAPI app onto Gradio
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7860)
