from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="FastAPI Shop - Cart System")

# --- 1. DATA MODELS ---
class CartItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: int
    subtotal: int

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

class Order(BaseModel):
    order_id: int
    customer_name: str
    product: str
    quantity: int
    total_price: int

# --- 2. DATABASE (In-Memory) ---
products = {
    1: {"name": "Wireless Mouse", "price": 499, "in_stock": True},
    2: {"name": "Notebook", "price": 99, "in_stock": True},
    3: {"name": "USB Hub", "price": 650, "in_stock": False},
    4: {"name": "Pen Set", "price": 49, "in_stock": True},
}

cart = []    # Stores CartItem dictionaries
orders = []  # Stores Order dictionaries

# --- 3. HELPER FUNCTIONS ---
def calculate_subtotal(price: int, qty: int):
    return price * qty

# --- 4. ENDPOINTS ---

@app.get("/products")
def get_products():
    return products

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):
    # Q3: Check if product exists (404)
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products[product_id]
    
    # Q3: Check if product is in stock (400)
    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # Q4: Check for duplicates (Update quantity instead of adding new entry)
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_subtotal(product["price"], item["quantity"])
            return {"message": "Cart updated", "cart_item": item}

    # Q1: Add new item to cart
    new_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": calculate_subtotal(product["price"], quantity)
    }
    cart.append(new_item)
    return {"message": "Added to cart", "cart_item": new_item}

@app.get("/cart")
def view_cart():
    # Q2: Confirm item_count and grand_total
    if not cart:
        return {"message": "Cart is empty", "items": [], "item_count": 0, "grand_total": 0}
    
    grand_total = sum(item["subtotal"] for item in cart)
    return {
        "items": cart,
        "item_count": len(cart), # Unique products
        "grand_total": grand_total
    }

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    # Q5: Remove specific item
    global cart
    initial_len = len(cart)
    cart = [item for item in cart if item["product_id"] != product_id]
    
    if len(cart) == initial_len:
        raise HTTPException(status_code=404, detail="Item not in cart")
    
    return {"message": f"Product {product_id} removed from cart"}

@app.post("/cart/checkout")
def checkout(details: CheckoutRequest):
    # BONUS: Handle empty cart checkout
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    # Q5 & Q6: Create orders for every item in cart
    new_orders_placed = []
    for item in cart:
        order_entry = {
            "order_id": len(orders) + 1,
            "customer_name": details.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }
        orders.append(order_entry)
        new_orders_placed.append(order_entry)

    # Clear the cart after checkout
    cart.clear()
    
    return {
        "message": "Order placed successfully",
        "orders_placed": new_orders_placed
    }

@app.get("/orders")
def get_all_orders():
    # Q6: View all historical orders
    return {"orders": orders, "total_orders": len(orders)}