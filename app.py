from fastapi import FastAPI

from autoguard_cf.demo import run

app = FastAPI(title="AutoGuard Counterfactual Lab", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/demo")
def demo() -> dict[str, object]:
    return run()
