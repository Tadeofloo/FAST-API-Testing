from fastapi import FastAPI, HTTPException
import time

app = FastAPI(title="Unstable API", version="1.0.0")

mem_leak_list = []

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/stress-cpu")
def stress_cpu():
    # Block CPU thread for 10 seconds to simulate load
    end_time = time.time() + 10
    while time.time() < end_time:
        pass
    return {"status": "cpu_stressed"}

@app.get("/memory-leak")
def memory_leak():
    # Allocate roughly 50MB of memory per request globally
    global mem_leak_list
    mem_leak_list.append(" " * (50 * 1024 * 1024))
    return {"status": "memory_allocated"}

@app.get("/force-error")
def force_error():
    # Simulate an unhandled exception for error rate monitoring
    raise HTTPException(status_code=500, detail="Intentional server error")