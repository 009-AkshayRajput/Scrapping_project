from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base  # ✅ important
from app.db import models       # ✅ VERY IMPORTANT LINE
from app.routers import auth, stocks, scrape
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(scrape.router)
