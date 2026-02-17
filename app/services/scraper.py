from playwright.sync_api import sync_playwright
from fastapi.concurrency import run_in_threadpool
from app.database import SessionLocal
from app.models import Stock


TARGET_URL = "https://groww.in/markets/top-volume"


def fetch_top_volume_stocks():
    """
    Scrapes top volume stocks from Groww website
    and returns structured stock data.
    """
    collected_data = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
        page = context.new_page()

        page.goto(TARGET_URL, timeout=60000)
        page.wait_for_selector("table tbody tr", timeout=60000)

        rows = page.query_selector_all("table tbody tr")

        for row in rows:
            try:
                company_element = row.query_selector("td:nth-child(2)")
                price_element = row.query_selector("td:nth-child(4)")
                volume_element = row.query_selector("td:nth-child(5)")

                if not all([company_element, price_element, volume_element]):
                    continue

                company_name = company_element.inner_text().split("\n")[0].strip()

                raw_price = price_element.inner_text()
                cleaned_price = (
                    raw_price.split("\n")[0]
                    .replace("₹", "")
                    .replace(",", "")
                    .strip()
                )

                raw_volume = volume_element.inner_text()
                cleaned_volume = (
                    raw_volume.replace(",", "")
                    .replace("Cr", "")
                    .replace("L", "")
                    .strip()
                )

                collected_data.append({
                    "company_name": company_name,
                    "price": float(cleaned_price),
                    "volume": int(float(cleaned_volume)) if cleaned_volume else 0
                })

            except Exception:
                # Skip faulty row but continue scraping
                continue

        browser.close()

    return collected_data


def save_or_update_stocks(stock_list):
    """
    Inserts new stock records or updates existing ones.
    Returns summary statistics.
    """
    db = SessionLocal()
    inserted_count = 0
    updated_count = 0

    try:
        for stock_data in stock_list:
            existing_stock = db.query(Stock).filter(
                Stock.company_name == stock_data["company_name"]
            ).first()

            if existing_stock:
                existing_stock.price = stock_data["price"]
                existing_stock.volume = stock_data["volume"]
                updated_count += 1
            else:
                new_stock = Stock(**stock_data)
                db.add(new_stock)
                inserted_count += 1

        db.commit()

    finally:
        db.close()

    return {
        "message": "Stock data processed successfully",
        "inserted": inserted_count,
        "updated": updated_count,
        "total_scraped": len(stock_list)
    }


def scrape_logic():
    """
    Complete scraping workflow:
    1. Fetch stock data
    2. Save to database
    3. Return summary
    """
    stocks = fetch_top_volume_stocks()
    return save_or_update_stocks(stocks)


async def scrape_stocks():
    """
    Async wrapper to run blocking scraping
    inside FastAPI without blocking event loop.
    """
    return await run_in_threadpool(scrape_logic)
