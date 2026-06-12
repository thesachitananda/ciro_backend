from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI(title="Ciro Quantity Enterprise Global SOR Engine")

# This master index maps out our initial state profiles natively
sor_cloud_database = {
    "Odisha": {
        "regionName": "Odisha PWD (OPWD)",
        "excavationRatePerCuM": 142.0,
        "brickworkBelowGlRatePerCuM": 4550.0,
        "brickworkSuperstructureRatePerCuM": 4800.0,
        "rccSorRatePerCuM": 6000.0,
        "shutteringRatePerSqM": 395.0,
        "rebarRatePerKg": 70.0,
        "flooringRatePerSqM": 780.0,
    },
    "Central_CPWD": {
        "regionName": "Central PWD (CPWD)",
        "excavationRatePerCuM": 160.0,
        "brickworkBelowGlRatePerCuM": 5100.0,
        "brickworkSuperstructureRatePerCuM": 5350.0,
        "rccSorRatePerCuM": 6500.0,
        "shutteringRatePerSqM": 450.0,
        "rebarRatePerKg": 75.0,
        "flooringRatePerSqM": 900.0,
    },
    "Maharashtra": {
        "regionName": "Maharashtra PWD",
        "excavationRatePerCuM": 175.0,
        "brickworkBelowGlRatePerCuM": 5250.0,
        "brickworkSuperstructureRatePerCuM": 5500.0,
        "rccSorRatePerCuM": 6850.0,
        "shutteringRatePerSqM": 475.0,
        "rebarRatePerKg": 78.0,
        "flooringRatePerSqM": 980.0,
    }
}

@app.get("/")
def home():
    return {"status": "Ciro Cloud Engine is active and running smoothly!"}

@app.get("/api/sor/v1")
async def get_regional_rates(state: str):
    """
    Delivers cached PWD rates directly from cloud memory in milliseconds
    """
    state_data = sor_cloud_database.get(state)
    if not state_data:
        raise HTTPException(status_code=404, detail=f"State '{state}' SOR profile not initialized yet.")
    
    return {
        **state_data,
        "lastSyncTimestamp": int(datetime.utcnow().timestamp() * 1000)
    }