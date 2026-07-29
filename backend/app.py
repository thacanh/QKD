import gradio as gr
import spaces
from fastapi import Request
from starlette.responses import JSONResponse
from main import health as fastapi_health
from main import simulate as fastapi_simulate
from main import SimulateRequest

# 1. Top-level @spaces.GPU function for HF ZeroGPU supervisor
@spaces.GPU
def predict_gpu(text: str):
    return f"QuantumShield ZeroGPU Online: {text}"

# 2. Standard Gradio Interface registering @spaces.GPU function
demo = gr.Interface(
    fn=predict_gpu,
    inputs=gr.Textbox(label="Status Input", value="Check"),
    outputs=gr.Textbox(label="Status Output"),
    title="QuantumShield FinEdu API Server",
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /v1/simulate, /api/simulate, /simulate",
)

# 3. Direct FastAPI route handlers on demo.app using Request to bypass Gradio Pydantic validation
async def handle_health(request: Request):
    res = await fastapi_health()
    return JSONResponse(res)

async def handle_simulate(request: Request):
    body = await request.json()
    if isinstance(body, dict) and "data" in body and isinstance(body["data"], list) and len(body["data"]) > 0:
        req_data = body["data"][0]
    else:
        req_data = body

    if isinstance(req_data, dict):
        req = SimulateRequest(**req_data)
    else:
        req = req_data

    res = await fastapi_simulate(req)
    return JSONResponse(res.model_dump())

# Register routes on demo.app for all path variants
for path in ["/v1/health", "/v1/health/", "/api/health", "/api/health/", "/health", "/health/"]:
    demo.app.add_api_route(path, handle_health, methods=["GET"])

for path in ["/v1/simulate", "/v1/simulate/", "/api/simulate", "/api/simulate/", "/simulate", "/simulate/"]:
    demo.app.add_api_route(path, handle_simulate, methods=["POST"])

# 4. Canonical Gradio launch call to satisfy HF ZeroGPU supervisor
if __name__ == "__main__":
    demo.launch()
else:
    demo.launch()
