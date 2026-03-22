from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ---------------- DATA ---------------- #
items = [
    {"id": 1, "name": "Tomato", "price": 40, "unit": "kg", "category": "Vegetable", "in_stock": True},
    {"id": 2, "name": "Milk", "price": 30, "unit": "litre", "category": "Dairy", "in_stock": True},
    {"id": 3, "name": "Apple", "price": 120, "unit": "kg", "category": "Fruit", "in_stock": True},
    {"id": 4, "name": "Rice", "price": 60, "unit": "kg", "category": "Grain", "in_stock": False},
    {"id": 5, "name": "Eggs", "price": 70, "unit": "dozen", "category": "Dairy", "in_stock": True},
    {"id": 6, "name": "Potato", "price": 30, "unit": "kg", "category": "Vegetable", "in_stock": True},
]

orders = []
order_counter = 1
cart = []

# ---------------- DAY 1 ---------------- #

@app.get("/")
def home():
    return {"message": "Welcome to FreshMart Grocery"}

@app.get("/items")
def get_items():
    in_stock_count = sum(1 for i in items if i["in_stock"])
    return {"items": items, "total": len(items), "in_stock_count": in_stock_count}

@app.get("/items/summary")
def summary():
    categories = {}
    for i in items:
        categories[i["category"]] = categories.get(i["category"], 0) + 1

    return {
        "total": len(items),
        "in_stock": sum(1 for i in items if i["in_stock"]),
        "out_of_stock": sum(1 for i in items if not i["in_stock"]),
        "categories": categories
    }

@app.get("/items/filter")
def filter_items(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    unit: Optional[str] = None,
    in_stock: Optional[bool] = None
):
    result = items

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if unit is not None:
        result = [i for i in result if i["unit"] == unit]

    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    return {"results": result, "count": len(result)}

@app.get("/items/search")
def search_items(keyword: str):
    result = [i for i in items if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]
    return {"results": result, "total_found": len(result)}

@app.get("/items/sort")
def sort_items(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(400, "Invalid sort_by")

    reverse = True if order == "desc" else False
    sorted_items = sorted(items, key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted": sorted_items}

@app.get("/items/page")
def paginate_items(page: int = 1, limit: int = 4):
    start = (page - 1) * limit
    end = start + limit
    total_pages = (len(items) + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": items[start:end]
    }

@app.get("/items/browse")
def browse_items(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = items.copy()

    # 🔍 keyword search (name + category)
    if keyword:
        result = [
            i for i in result
            if keyword.lower() in i["name"].lower()
            or keyword.lower() in i["category"].lower()
        ]

    # 🧱 category filter (case insensitive)
    if category:
        result = [i for i in result if i["category"].lower() == category.lower()]

    # 📦 stock filter
    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    # ❗ validate sort_by
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(400, "Invalid sort_by")

    # ↕ sorting
    result = sorted(
        result,
        key=lambda x: x[sort_by],
        reverse=(order == "desc")
    )

    # 📄 pagination
    start = (page - 1) * limit
    end = start + limit
    total_pages = (len(result) + limit - 1) // limit

    return {
        "total": len(result),
        "total_pages": total_pages,
        "page": page,
        "data": result[start:end]
    }
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for i in items:
        if i["id"] == item_id:
            return i
    raise HTTPException(404, "Item not found")
# 🔍 SEARCH ORDERS
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer"].lower()
    ]
    return {"total_found": len(result), "orders": result}


# ↕ SORT ORDERS
@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    sorted_orders = sorted(
        orders,
        key=lambda x: x["total_cost"],
        reverse=True if order == "desc" else False
    )
    return {"orders": sorted_orders}


# 📄 PAGINATION ORDERS
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    total = len(orders)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total": len(orders)}



class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)
    delivery_address: str = Field(..., min_length=10)
    delivery_slot: str = "Morning"
    bulk_order: bool = False

class NewItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    unit: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    in_stock: bool = True



def find_item(item_id):
    for i in items:
        if i["id"] == item_id:
            return i
    return None

def calculate_total(price, quantity, slot, bulk):
    total = price * quantity
    original = total

    if bulk and quantity >= 10:
        total *= 0.92

    if slot == "Morning":
        total += 40
    elif slot == "Evening":
        total += 60

    return original, round(total, 2)



@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_item(order.item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    if not item["in_stock"]:
        raise HTTPException(400, "Out of stock")

    original, total = calculate_total(item["price"], order.quantity, order.delivery_slot, order.bulk_order)

    new_order = {
        "order_id": order_counter,
        "customer": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_cost": total,
        "original_cost": original,
        "status": "confirmed"
    }

    orders.append(new_order)
    order_counter += 1
    return new_order

@app.post("/items", status_code=201)
def add_item(item: NewItem):
    for i in items:
        if i["name"].lower() == item.name.lower():
            raise HTTPException(400, "Duplicate item")

    new = {"id": len(items) + 1, **item.dict()}
    items.append(new)
    return new

@app.put("/items/{item_id}")
def update_item(item_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):
    item = find_item(item_id)
    if not item:
        raise HTTPException(404, "Not found")

    if price is not None:
        item["price"] = price
    if in_stock is not None:
        item["in_stock"] = in_stock

    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(404, "Not found")

    for o in orders:
        if o["item"] == item["name"]:
            raise HTTPException(400, "Active orders exist")

    items.remove(item)
    return {"message": "Deleted successfully"}



@app.post("/cart/add")
def add_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)

    if not item or not item["in_stock"]:
        raise HTTPException(400, "Item unavailable")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return c

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"message": "Added to cart"}

@app.get("/cart")
def view_cart():
    total = 0
    details = []

    for c in cart:
        item = find_item(c["item_id"])
        subtotal = item["price"] * c["quantity"]
        total += subtotal

        details.append({
            "item": item["name"],
            "quantity": c["quantity"],
            "subtotal": subtotal
        })

    return {"cart": details, "grand_total": total}

@app.delete("/cart/{item_id}")
def remove_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Removed"}
    raise HTTPException(404, "Item not in cart")

@app.post("/cart/checkout", status_code=201)
def checkout(name: str, address: str, slot: str):
    global order_counter

    if not cart:
        raise HTTPException(400, "Cart empty")

    result = []
    total = 0

    for c in cart:
        item = find_item(c["item_id"])
        cost = item["price"] * c["quantity"]

        order = {
            "order_id": order_counter,
            "customer": name,
            "item": item["name"],
            "total_cost": cost
        }

        orders.append(order)
        result.append(order)
        total += cost
        order_counter += 1

    cart.clear()

    return {"orders": result, "grand_total": total}