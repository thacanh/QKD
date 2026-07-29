import gradio as gr
import spaces
from fastapi import Request
from main import health as fastapi_health
from main import simulate as fastapi_simulate
from main import SimulateRequest

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
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /api/health and /api/simulate",
)

# Direct FastAPI endpoint registrations on Gradio's internal FastAPI app
@demo.app.get("/api/health")
async def health_endpoint():
    return await fastapi_health()

@demo.app.post("/api/simulate")
async def simulate_endpoint(request: Request):
    body = await request.json()
    # Support both raw JSON from Vercel and Gradio-wrapped data payload
    if isinstance(body, dict) and "data" in body and isinstance(body["data"], list) and len(body["data"]) > 0:
        req_data = body["data"][0]
    else:
        req_data = body
    
    if isinstance(req_data, dict):
        req = SimulateRequest(**req_data)
    else:
        req = req_data
        
    return await fastapi_simulate(req)

# Launch demo to keep thread running continuously for HF Space runner
if __name__ == "__main__":
    demo.launch()
else:
    demo.launch()
