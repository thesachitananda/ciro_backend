from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 📦 Added for static file hosting
from datetime import datetime
import os

app = FastAPI(title="Ciro Advanced Structural Engine Cluster")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🗺️ Master Verified Schedule of Rates Database
sor_cloud_database = {
    "Odisha": {
        "regionName": "Odisha PWD (OPWD)",
        "rateExcavationSoftSoilManual": 125.0, "rateExcavationHardSoilManual": 165.0,
        "rateExcavationSoftRockManual": 290.0, "rateExcavationMechanical": 75.0,
        "pccRatePerCuM": 4200.0, "footingRatePerCuM": 5800.0, "pedestalRatePerCuM": 6000.0,
        "beamRatePerCuM": 6200.0, "columnRatePerCuM": 6500.0, "slabRatePerCuM": 6100.0,
        "brickworkBelowGlRatePerCuM": 4550.0, "brickworkSuperstructureRatePerCuM": 4800.0,
        "shutteringRatePerSqM": 395.0, "rebarRatePerKg": 70.0, "plasteringRatePerSqM": 180.0, "flooringRatePerSqM": 780.0,
        "laborMultiplierExcavation": 1.2, "laborMultiplierConcrete": 2.5, "laborMultiplierBrickwork": 3.1
    },
    "Chhattisgarh": {
        "regionName": "Chhattisgarh PWD",
        "rateExcavationSoftSoilManual": 115.0, "rateExcavationHardSoilManual": 155.0,
        "rateExcavationSoftRockManual": 275.0, "rateExcavationMechanical": 70.0,
        "pccRatePerCuM": 4000.0, "footingRatePerCuM": 5600.0, "pedestalRatePerCuM": 5800.0,
        "beamRatePerCuM": 6000.0, "columnRatePerCuM": 6200.0, "slabRatePerCuM": 5900.0,
        "brickworkBelowGlRatePerCuM": 4350.0, "brickworkSuperstructureRatePerCuM": 4600.0,
        "shutteringRatePerSqM": 375.0, "rebarRatePerKg": 67.0, "plasteringRatePerSqM": 165.0, "flooringRatePerSqM": 740.0,
        "laborMultiplierExcavation": 1.15, "laborMultiplierConcrete": 2.4, "laborMultiplierBrickwork": 2.95
    },
    "Andhra_Pradesh": {
        "regionName": "Andhra Pradesh PWD",
        "rateExcavationSoftSoilManual": 130.0, "rateExcavationHardSoilManual": 170.0,
        "rateExcavationSoftRockManual": 305.0, "rateExcavationMechanical": 80.0,
        "pccRatePerCuM": 4300.0, "footingRatePerCuM": 5900.0, "pedestalRatePerCuM": 6100.0,
        "beamRatePerCuM": 6300.0, "columnRatePerCuM": 6600.0, "slabRatePerCuM": 6200.0,
        "brickworkBelowGlRatePerCuM": 4600.0, "brickworkSuperstructureRatePerCuM": 4900.0,
        "shutteringRatePerSqM": 410.0, "rebarRatePerKg": 71.0, "plasteringRatePerSqM": 190.0, "flooringRatePerSqM": 800.0,
        "laborMultiplierExcavation": 1.25, "laborMultiplierConcrete": 2.65, "laborMultiplierBrickwork": 3.2
    },
    "Delhi_CPWD": {
        "regionName": "Central PWD (CPWD)",
        "rateExcavationSoftSoilManual": 145.0, "rateExcavationHardSoilManual": 190.0,
        "rateExcavationSoftRockManual": 330.0, "rateExcavationMechanical": 90.0,
        "pccRatePerCuM": 4500.0, "footingRatePerCuM": 6200.0, "pedestalRatePerCuM": 6500.0,
        "beamRatePerCuM": 6650.0, "columnRatePerCuM": 6900.0, "slabRatePerCuM": 6400.0,
        "brickworkBelowGlRatePerCuM": 5100.0, "brickworkSuperstructureRatePerCuM": 5350.0,
        "shutteringRatePerSqM": 450.0, "rebarRatePerKg": 75.0, "plasteringRatePerSqM": 210.0, "flooringRatePerSqM": 900.0,
        "laborMultiplierExcavation": 1.35, "laborMultiplierConcrete": 2.8, "laborMultiplierBrickwork": 3.5
    }
}

for key in sor_cloud_database:
    sor_cloud_database[key]["lastSyncTimestamp"] = int(datetime.utcnow().timestamp() * 1000)

# 📁 Ensure local runtime directories exist in the cloud container before mounting
os.makedirs("static/banners", exist_ok=True)

# 🌐 MOUNT ROUTE: This maps the directory folder to public web streams
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(): 
    return {"status": "Ciro Advanced Civil Engine Connected Deployment Online"}

@app.get("/api/sor/v1")
async def get_regional_rates(state: str):
    state_data = sor_cloud_database.get(state)
    if not state_data: 
        raise HTTPException(status_code=404, detail="State context matrix vector not found.")
    return state_data

@app.get("/api/tenders/v1")
async def get_live_pwd_tenders():
    return {"status": "Redirection Protocol Enabled On-Device", "tenders": []}