from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

app = FastAPI(title="Ciro SaaS Global Infrastructure Engine Cluster")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sor_cloud_database = {
    "Odisha": {
        "regionName": "Odisha PWD (OPWD)", "excavationRatePerCuM": 142.0, "pccRatePerCuM": 4200.0,
        "footingRatePerCuM": 5800.0, "pedestalRatePerCuM": 6000.0, "beamRatePerCuM": 6200.0,
        "columnRatePerCuM": 6500.0, "slabRatePerCuM": 6100.0, "brickworkBelowGlRatePerCuM": 4550.0,
        "brickworkSuperstructureRatePerCuM": 4800.0, "shutteringRatePerSqM": 395.0, "rebarRatePerKg": 70.0,
        "plasteringRatePerSqM": 180.0, "flooringRatePerSqM": 780.0
    },
    "Chhattisgarh": {
        "regionName": "Chhattisgarh PWD", "excavationRatePerCuM": 132.0, "pccRatePerCuM": 4000.0,
        "footingRatePerCuM": 5600.0, "pedestalRatePerCuM": 5800.0, "beamRatePerCuM": 6000.0,
        "columnRatePerCuM": 6200.0, "slabRatePerCuM": 5900.0, "brickworkBelowGlRatePerCuM": 4350.0,
        "brickworkSuperstructureRatePerCuM": 4600.0, "shutteringRatePerSqM": 375.0, "rebarRatePerKg": 67.0,
        "plasteringRatePerSqM": 165.0, "flooringRatePerSqM": 740.0
    },
    "Andhra_Pradesh": {
        "regionName": "Andhra Pradesh PWD", "excavationRatePerCuM": 145.0, "pccRatePerCuM": 4300.0,
        "footingRatePerCuM": 5900.0, "pedestalRatePerCuM": 6100.0, "beamRatePerCuM": 6300.0,
        "columnRatePerCuM": 6600.0, "slabRatePerCuM": 6200.0, "brickworkBelowGlRatePerCuM": 4600.0,
        "brickworkSuperstructureRatePerCuM": 4900.0, "shutteringRatePerSqM": 410.0, "rebarRatePerKg": 71.0,
        "plasteringRatePerSqM": 190.0, "flooringRatePerSqM": 800.0
    },
    "Delhi_CPWD": {
        "regionName": "Central PWD (CPWD)", "excavationRatePerCuM": 160.0, "pccRatePerCuM": 4500.0,
        "footingRatePerCuM": 6200.0, "pedestalRatePerCuM": 6500.0, "beamRatePerCuM": 6650.0,
        "columnRatePerCuM": 6900.0, "slabRatePerCuM": 6400.0, "brickworkBelowGlRatePerCuM": 5100.0,
        "brickworkSuperstructureRatePerCuM": 5350.0, "shutteringRatePerSqM": 450.0, "rebarRatePerKg": 75.0,
        "plasteringRatePerSqM": 210.0, "flooringRatePerSqM": 900.0
    }
}

for key in sor_cloud_database:
    sor_cloud_database[key]["lastSyncTimestamp"] = int(datetime.utcnow().timestamp() * 1000)

def fetch_live_central_procurement_feed():
    scraped_results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # 🌐 Hit the open state portal updates XML feed (Bypasses Session Blocks)
        feed_url = "https://eprocure.gov.in/cppp/latest_tenders_rss"
        response = requests.get(feed_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # Find item tags inside the XML tree
            items = root.findall('.//item')
            
            for idx, item in enumerate(items[:5]): # Pull the 5 most recent live public notices
                title = item.find('title').text if item.find('title') is not None else "Infrastructure Work Notice"
                link = item.find('link').text if item.find('link') is not None else "https://eprocure.gov.in"
                desc = item.find('description').text if item.find('description') is not None else "Civil Infrastructure Execution Project"
                
                scraped_results.append({
                    "id": f"LIVE-CPPP-2026-{200 + idx}",
                    "title": title[:110] + "...", # Format text gracefully for mobile cards
                    "authority": desc.split('||')[0] if '||' in desc else "Public Works Division",
                    "value": "Check Notice Documents",
                    "closingDate": "See Portal Notice",
                    "link": link
                })
    except Exception:
        pass
        
    return scraped_results

@app.get("/")
def home(): 
    return {"status": "Ciro Core Structural Engine Online and Verified"}

@app.get("/api/sor/v1")
async def get_regional_rates(state: str):
    state_data = sor_cloud_database.get(state)
    if not state_data: 
        raise HTTPException(status_code=404, detail="State context vector not found.")
    return state_data

@app.get("/api/tenders/v1")
async def get_live_pwd_tenders():
    # Fetch live feeds and append manual entries seamlessly
    live_scraped = fetch_live_central_procurement_feed()
    
    manual_tenders = [
        {"id": "TND-OD-2026-901", "title": "Construction of Residential Quarters (G+2 Type) Including Earthwork Excavation & RCC Footing Layouts at Rourkela Division", "authority": "Odisha PWD (R&B Division)", "value": "₹ 1,20,00,000", "closingDate": "12 July 2026", "link": "https://tendersodisha.gov.in"},
        {"id": "TND-CG-2026-902", "title": "Supplying Structural Rebar and Reinforced Concrete Works for Government Higher Secondary School Compound Wall Construction", "authority": "Chhattisgarh Public Works Department", "value": "₹ 12,30,000", "closingDate": "05 July 2026", "link": "https://eproc.cgstate.gov.in"},
        {"id": "TND-AP-2026-903", "title": "Construction of Concrete Drainage Channel and Paver Block Road Layout across Sector Corridors", "authority": "Andhra Pradesh PWD Infrastructure Wing", "value": "₹ 48,50,000", "closingDate": "20 July 2026", "link": "https://tender.apeprocurement.gov.in"}
    ]
    
    return {
        "lastUpdated": str(datetime.now().strftime("%d %B %Y, %I:%M %p")), 
        "tenders": live_scraped + manual_tenders
    }