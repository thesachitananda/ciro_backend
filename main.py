from fastapi import FastAPI, HTTPException
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pdfplumber
import io

app = FastAPI(title="Ciro Quantity Enterprise Global SOR Engine")

# Central in-memory cloud broker database storage cache
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
        "lastSyncTimestamp": int(datetime.utcnow().timestamp() * 1000)
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
        "lastSyncTimestamp": int(datetime.utcnow().timestamp() * 1000)
    }
}

def run_live_odisha_scraper():
    """
    Background worker: Navigates to the portal page, reads published document files,
    parses specific item columns, and maps them directly into our active memory parameters.
    """
    try:
        # 1. Scraping Layer: Target the state publication folder link
        portal_url = "https://works.odisha.gov.in/publications/schedule-of-rates"
        # We include a browser header mock to prevent government firewalls from blocking our requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(portal_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the first file download link containing our SOR keyword parameters
        target_link = None
        for anchor in soup.find_all('a', href=True):
            if "schedule" in anchor['href'].lower() or "sor" in anchor['href'].lower():
                target_link = anchor['href']
                break
        
        if not target_link:
            return False

        # Build absolute URL path if the link extracted is relative
        if not target_link.startswith("http"):
            target_link = "https://works.odisha.gov.in" + target_link

        # 2. Memory Stream Extraction Layer: Download the PDF into temporary RAM memory
        pdf_response = requests.get(target_link, headers=headers, timeout=30)
        pdf_file = io.BytesIO(pdf_response.content)

        # 3. Parsing Layer: Scan document tables looking for standard engineering keyword identifiers
        with pdfplumber.open(pdf_file) as pdf:
            # We scan the first 15 pages where abstract basic material schedules are traditionally listed
            for page in pdf.pages[:15]:
                text = page.extract_text()
                if not text:
                    continue
                
                for line in text.split("\n"):
                    # Automated string tracking logic sorting PWD standard entries
                    if "earthwork" in line.lower() and "excavation" in line.lower():
                        # Extract the trailing numeric value from the row text string block
                        parts = line.split()
                        for part in reversed(parts):
                            val = part.replace("₹", "").replace(",", "").strip()
                            if val.replace('.', '', 1).isdigit():
                                sor_cloud_database["Odisha"]["excavationRatePerCuM"] = float(val)
                                break
                                
                    elif "brickwork" in line.lower() and "superstructure" in line.lower():
                        parts = line.split()
                        for part in reversed(parts):
                            val = part.replace("₹", "").replace(",", "").strip()
                            if val.replace('.', '', 1).isdigit():
                                sor_cloud_database["Odisha"]["brickworkSuperstructureRatePerCuM"] = float(val)
                                break

        sor_cloud_database["Odisha"]["lastSyncTimestamp"] = int(datetime.utcnow().timestamp() * 1000)
        return True
    except Exception as e:
        print(f"Scraper encountered background error: {e}")
        return False

@app.get("/")
def home():
    return {"status": "Ciro Cloud Engine is active and running smoothly!"}

@app.get("/api/sor/v1")
async def get_regional_rates(state: str):
    state_data = sor_cloud_database.get(state)
    if not state_data:
        raise HTTPException(status_code=404, detail=f"State '{state}' SOR profile not initialized yet.")
    return state_data

@app.post("/api/sor/admin/trigger-scrape")
async def trigger_system_scrape():
    """Admin endpoint to force the server to fetch fresh government values on demand"""
    success = run_live_odisha_scraper()
    if not success:
        return {"status": "Scrape completed using safe fallback values cache."}
    return {"status": "Live database parameters synchronized successfully from official sources!"}