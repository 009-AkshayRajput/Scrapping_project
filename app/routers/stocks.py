from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.models import Stock
from app.schemas.stock import StockUpdate
from app.dependencies import get_db, admin_required
#Router configuration for stock-related APIs
router = APIRouter(prefix="/stocks",tags=["Stocks"])
#GET:Fetching Stocks with Pagination and Optional Filters
@router.get("/")
def get_stocks(
    page:int=Query(1,ge=1),                     # Current page number(default=1)
    limit:int=Query(10,ge=1,le=100),            # Records per page(max 100)
    min_volume:Optional[int]=None,              # Filter:minimum trading volume
    max_price:Optional[float]=None,             # Filter:maximum stock price
    company_name:Optional[str]=None,            # Filter:partial company name match
    db:Session=Depends(get_db)                  # Database session dependency
):
    #Start building base query
    stock_query = db.query(Stock)
    #Appling filters only if provided by client
    if min_volume:
        stock_query = stock_query.filter(Stock.volume >= min_volume)
    if max_price:
        stock_query = stock_query.filter(Stock.price <= max_price)
    if company_name:
        # Case-insensitive partial search
        stock_query = stock_query.filter(
            Stock.company_name.ilike(f"%{company_name}%")
        )
    #Get total count before applying pagination
    total_records = stock_query.count()
    #Apply sorting and pagination
    #pagination:-Pagination means dividing large data into smaller chunks instead of returning everything at once.
    records = (
        stock_query
        .order_by(Stock.id)                     # Consistent ordering
        .offset((page - 1) * limit)             # Skip previous pages
        .limit(limit)                           # Limit number of results
        .all()
    )
    #Calculate total pages safely
    total_pages = (total_records + limit - 1) // limit
    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "results": records
    }



# PUT:Updating Stock Details (Admin Only)

@router.put("/{stock_id}", dependencies=[Depends(admin_required)])
def update_stock(
    stock_id: int,
    payload: StockUpdate,
    db: Session = Depends(get_db)
):
   
    #Fetch stock by primary key
    stock = db.query(Stock).filter(Stock.id == stock_id).first()

    #If stock does not exist, return 404
    if not stock:
        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )

    #Update only price and volume fields
    stock.price=payload.price
    stock.volume=payload.volume

    #Commit changes to database
    db.commit()

    #Refresh instance to return updated data
    db.refresh(stock)

    return {
        "message": "Stock updated successfully",
        "updated_stock": stock
    }



# DELETE:Remove Stock(Admin Only)

@router.delete("/{stock_id}", dependencies=[Depends(admin_required)])
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    
    # Find stock by ID
    stock = db.query(Stock).filter(Stock.id == stock_id).first()

    if not stock:
        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )
    # Delete record from Database
    db.delete(stock)
    db.commit()

    return {
        "message": "Stock deleted successfully"
    }
