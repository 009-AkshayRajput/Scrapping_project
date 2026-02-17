from fastapi import APIRouter
from app.services.scraper import scrape_stocks

router = APIRouter(prefix="/scrape", tags=["Scrape"])
@router.post("/")
async def scrape():
    result = await scrape_stocks()
    return result

# @router.post("/")
# async def scrape():
#     try:
#         result = await scrape_stocks()
#         return result
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return {"error": str(e)}
