from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI()

# --- Mock Data ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 3, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []

# --- Existing Endpoints (Q1 - Q3) ---

@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    results = [p for p in products if keyword.lower() in p['name'].lower()]
    if not results:
        return {"message": f"No products found for: {keyword}"}
    return {"keyword": keyword, "total_found": len(results), "products": results}

@app.get("/products/sort")
def sort_products(sort_by: str = Query("price"), order: str = Query("asc")):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")
    
    is_reverse = (order == "desc")
    sorted_data = sorted(products, key=lambda p: p[sort_by], reverse=is_reverse)
    return {"sort_by": sort_by, "order": order, "products": sorted_data}

@app.get("/products/page")
def paginate_products(page: int = Query(1, ge=1), limit: int = Query(2, ge=1)):
    start = (page - 1) * limit
    end = start + limit
    paged_data = products[start:end]
    total_pages = -(-len(products) // limit) # Ceiling division
    return {
        "page": page, 
        "limit": limit, 
        "total_pages": total_pages, 
        "products": paged_data
    }

# --- New Assignment Endpoints (Q4 - Q6 + Bonus) ---

# Q4: Search Orders
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    results = [o for o in orders if customer_name.lower() in o['customer_name'].lower()]
    if not results:
        return {"message": f"No orders found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(results), "orders": results}

# Q5: Sort by Category (Alphabetical) then Price (Ascending)
@app.get("/products/sort-by-category")
def sort_by_category():
    # Sorts by category first, then price within that category
    result = sorted(products, key=lambda p: (p['category'], p['price']))
    return {"products": result, "total": len(result)}

# Q6: The "All-in-One" Browse Endpoint
@app.get("/products/browse")
def browse_products(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20)
):
    # 1. Search/Filter
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]
    
    # 2. Sort
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))
    
    # 3. Paginate
    total_found = len(result)
    total_pages = -(-total_found // limit)
    start = (page - 1) * limit
    paged_result = result[start : start + limit]
    
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_found": total_found,
            "total_pages": total_pages
        },
        "products": paged_result
    }

# ⭐ Bonus: Paginate Orders
@app.get("/orders/page")
def paginate_orders(page: int = Query(1, ge=1), limit: int = Query(3, ge=1)):
    start = (page - 1) * limit
    total_pages = -(-len(orders) // limit)
    return {
        "page": page,
        "limit": limit,
        "total_orders": len(orders),
        "total_pages": total_pages,
        "orders": orders[start : start + limit]
    }

# POST Endpoint to help you add data for testing
@app.post("/orders")
def create_order(order: dict):
    orders.append(order)
    return {"message": "Order added", "order": order}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product