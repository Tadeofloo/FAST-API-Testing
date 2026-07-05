import os
import gc
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Global list to simulate a controlled memory leak later
leak_storage = []

@app.get("/")
def read_root():
    environment = os.getenv("ENVIRONMENT", "development")
    return {
        "message": "Cloud Platform Microservice App",
        "environment": environment,
        "status": "operational"
    }

@app.get("/health")
def health_check():
    # Standard health check endpoint for Kubernetes probes
    return {"status": "healthy"}

@app.get("/stress-cpu")
def stress_cpu(iterations: int = 5_000_000):
    # Endpoint to simulate a CPU spike and trigger auto-scaling rules
    count = 0
    for i in range(iterations):
        count += i
    return {"message": "CPU load simulation complete", "result": count}

@app.get("/memory-leak")
def memory_leak(blocks: int = 10):
    # Endpoint to simulate memory exhaustion and trigger OOMKilled events
    global leak_storage
    try:
        for _ in range(blocks):
            # Allocate a chunk of memory (approx 10MB per block)
            large_string = "X" * (10 * 1024 * 1024)
            leak_storage.append(large_string)
        return {"message": f"Allocated {blocks} memory blocks successfully"}
    except MemoryError:
        raise HTTPException(status_code=500, detail="Application ran out of memory")

@app.get("/force-error")
def force_error():
    # Endpoint to force a 500 internal server error for observability metrics
    raise HTTPException(status_code=500, detail="Simulated application failure")