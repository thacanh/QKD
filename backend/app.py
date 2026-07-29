import os
import gradio as gr
from main import health as fastapi_health
from main import simulate as fastapi_simulate
from main import SimulateRequest

# Create standard Gradio Interface for HF Space
demo = gr.Interface(
    fn=lambda text: f"QuantumShield Backend Online: {text}",
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /api/health and /api/simulate",
)

# Direct FastAPI endpoint registrations on Gradio's internal FastAPI app
@demo.app.get("/api/health")
async def health_endpoint():
    return await fastapi_health()

@demo.app.post("/api/simulate")
async def simulate_endpoint(req: SimulateRequest):
    return await fastapi_simulate(req)
