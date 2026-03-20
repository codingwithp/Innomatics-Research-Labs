from fastapi import FastAPI, Query
app = FastAPI()
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]
orders = []
order_counter = 1
@app.get("/products")
def get_products():
    return {"products": products}
@app.get("/products/search")
def search_products(keyword: str):
    result = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(
        products,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):
    total = len(products)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": products[start:end]
    }
@app.get("/products/sort-by-category")
def sort_by_category():
    sorted_products = sorted(
        products,
        key=lambda x: (x["category"].lower(), x["price"])
    )
    return {"products": sorted_products}
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products

    # 🔍 Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # ↕ Sort
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # 📄 Pagination
    total = len(result)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": total_pages,
        "products": paginated
    }
@app.post("/orders")
def create_order(customer_name: str):
    global order_counter

    order = {
        "order_id": order_counter,
        "customer_name": customer_name,
        "items": products  # simple demo (all products)
    }

    orders.append(order)
    order_counter += 1

    return {"message": "Order placed", "order": order}
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):
    total = len(orders)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_orders": total,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}