from playwright.sync_api import sync_playwright
from app.database import SessionLocal
from app.models import Stock
from fastapi.concurrency import run_in_threadpool


def scrape_logic():
    url = "https://groww.in/markets/top-volume"
    stocks = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("table tbody tr", timeout=60000)

        rows = page.query_selector_all("table tbody tr")

        for row in rows:
            name_el = row.query_selector("td:nth-child(2)")
            price_el = row.query_selector("td:nth-child(4)")
            volume_el = row.query_selector("td:nth-child(5)")

            if name_el and price_el and volume_el:
                raw_name = name_el.inner_text()
                raw_price = price_el.inner_text()
                raw_volume = volume_el.inner_text()

                name = raw_name.split("\n")[0].strip()

                # Clean price
                price_value = (
                    raw_price.split("\n")[0]
                    .replace("₹", "")
                    .replace(",", "")
                    .strip()
                )

                # Clean volume
                volume_value = (
                    raw_volume.replace(",", "")
                    .replace("Cr", "")
                    .replace("L", "")
                    .strip()
                )

                stocks.append({
                    "name": name,
                    "price": float(price_value),
                    "volume": int(float(volume_value)) if volume_value else 0
                })

        browser.close()

    # ===== DB INSERT =====
    db = SessionLocal()
    new_records = 0
    existing_records = 0

    for item in stocks:
        existing = db.query(Stock).filter(
            Stock.company_name == item["name"]
        ).first()

        if existing:
            existing.price = item["price"]
            existing.volume = item["volume"]
            existing_records += 1
        else:
            stock = Stock(
                company_name=item["name"],
                price=item["price"],
                volume=item["volume"]
            )
            db.add(stock)
            new_records += 1

    db.commit()
    db.close()

    return {
        "message": "Scraping completed successfully",
        "new_records": new_records,
        "existing_records": existing_records,
        "total_scraped": len(stocks)
    }


async def scrape_stocks():
    return await run_in_threadpool(scrape_logic)
