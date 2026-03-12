from fastapi import FastAPI, Query, Path, Response, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# --- Mock Data ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

# --- Models ---
class NewProduct(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(...)
    in_stock: bool = True

# --- Helper Function ---
def find_product(product_id: int):
    return next((p for p in products if p["id"] == product_id), None)

# --- 1. GET All Products ---
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

# --- 5. Audit Endpoint (Must be ABOVE /{product_id}) ---
@app.get("/products/audit")
def product_audit():
    in_stock_list = [p for p in products if p['in_stock']]
    out_stock_list = [p for p in products if not p['in_stock']]
    stock_value = sum(p['price'] * 10 for p in in_stock_list)
    priciest = max(products, key=lambda p: p['price'])
    
    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p['name'] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {"name": priciest['name'], "price": priciest['price']}
    }

# --- Bonus: Bulk Discount (Must be ABOVE /{product_id}) ---
@app.put('/products/discount')
def bulk_discount(
    category: str = Query(..., description='Category to discount'),
    discount_percent: int = Query(..., ge=1, le=99, description='% off')
):
    updated = []
    for p in products:
        if p['category'].lower() == category.lower():
            p['price'] = int(p['price'] * (1 - discount_percent / 100))
            updated.append(p)
    
    if not updated:
        return {'message': f'No products found in category: {category}'}
    
    return {
        'message': f'{discount_percent}% discount applied to {category}',
        'updated_count': len(updated),
        'updated_products': updated
    }

# --- 2. GET Product by ID ---
@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    return product

# --- 1. POST (Add Product) ---
@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(data: NewProduct, response: Response):
    # Check for duplicate names
    if any(p["name"].lower() == data.name.lower() for p in products):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"Product '{data.name}' already exists"}
    
    new_id = max(p["id"] for p in products) + 1
    product_dict = data.model_dump()
    product_dict["id"] = new_id
    products.append(product_dict)
    return {"message": "Product added", "product": product_dict}

# --- 2. PUT (Update Product) ---
@app.put("/products/{product_id}")
def update_product(
    product_id: int, 
    response: Response,
    price: Optional[int] = Query(None),
    in_stock: Optional[bool] = Query(None)
):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    
    if price is not None:
        product["price"] = price
    if in_stock is not None:
        product["in_stock"] = in_stock
        
    return {"message": "Product updated", "product": product}

# --- 3. DELETE Product ---
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    
    products.remove(product)
    return {"message": f"Product '{product['name']}' deleted"}