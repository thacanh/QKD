import gradio as gr
import spaces
from starlette.responses import JSONResponse
from starlette.routing import Route
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
    description="Backend for CV-QKD / FSO simulation. API Endpoints active at /v1/health and /v1/simulate",
)

# Raw Starlette endpoint handlers bypassing Gradio's Pydantic validation
async def raw_health(request):
    res = await fastapi_health()
    return JSONResponse(res)

async def raw_simulate(request):
    body = await request.json()
    # Support both raw JSON payload from Vercel and Gradio-wrapped data payload
    if isinstance(body, dict) and "data" in body and isinstance(body["data"], list) and len(body["data"]) > 0:
        req_data = body["data"][0]
    else:
        req_data = body

    req = SimulateRequest(**req_data)
    res = await fastapi_simulate(req)
    return JSONResponse(res.model_dump())

# Insert all route variants at position 0 to match with or without trailing slashes and prefixes
for path in ["/v1/health", "/v1/health/", "/api/health", "/api/health/", "/health", "/health/"]:
    demo.app.router.routes.insert(0, Route(path, raw_health, methods=["GET"]))

for path in ["/v1/simulate", "/v1/simulate/", "/api/simulate", "/api/simulate/", "/simulate", "/simulate/"]:
    demo.app.router.routes.insert(0, Route(path, raw_simulate, methods=["POST"]))

# Launch demo to keep thread running continuously for HF Space runner
if __name__ == "__main__":
    demo.launch()
else:
    demo.launch()
