import gradio as gr
import spaces
from main import app as fastapi_app

# 1. Top-level function decorated with @spaces.GPU for HF ZeroGPU daemon
@spaces.GPU
def predict(prompt: str):
    return f"QuantumShield Backend Online: {prompt}"

# 2. Standard Gradio Interface registering the @spaces.GPU function
demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /api/health and /api/simulate",
)

# 3. Mount FastAPI app onto Gradio cleanly
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    demo.launch()
