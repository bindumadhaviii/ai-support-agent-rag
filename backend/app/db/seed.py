"""Fill the database with a small fake store for development and testing.

Run from the backend folder:  uv run python -m app.db.seed
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import text

from app.db.models import Customer, Order, OrderItem, OrderStatus, Product
from app.db.session import SessionLocal

NOW = datetime.now(timezone.utc).replace(tzinfo=None)


def days_ago(days: int) -> datetime:
    return NOW - timedelta(days=days)


PRODUCTS = [
    # sku, name, category, price
    ("JKT-001", "Alpine Insulated Jacket", "outerwear", "189.00"),
    ("BOOT-002", "Trailhead Waterproof Boots", "footwear", "149.00"),
    ("TENT-003", "Summit 2-Person Tent", "camping", "329.00"),
    ("BAG-004", "Ridge 40L Backpack", "bags", "119.00"),
    ("SOCK-005", "Merino Hiking Socks (3-pack)", "accessories", "24.00"),
    ("LAMP-006", "Basecamp Rechargeable Lantern", "camping", "45.00"),
]

CUSTOMERS = [
    # name, email
    ("Priya Sharma", "priya@example.com"),
    ("Marcus Lee", "marcus@example.com"),
    ("Elena Garcia", "elena@example.com"),
    ("James Okafor", "james@example.com"),
    ("Sofia Rossi", "sofia@example.com"),
]

ORDERS = [
    # customer email, status, ordered (days ago), delivered (days ago), tracking, [(sku, qty)]
    ("priya@example.com", OrderStatus.delivered, 9, 5, "TRK100001", [("JKT-001", 1)]),
    ("marcus@example.com", OrderStatus.delivered, 50, 45, "TRK100002", [("BOOT-002", 1)]),
    ("elena@example.com", OrderStatus.shipped, 3, None, "TRK100003", [("TENT-003", 1)]),
    ("james@example.com", OrderStatus.pending, 0, None, None, [("SOCK-005", 2), ("LAMP-006", 1)]),
    ("sofia@example.com", OrderStatus.delivered, 14, 10, "TRK100005", [("TENT-003", 1), ("BAG-004", 1)]),
    ("priya@example.com", OrderStatus.refunded, 40, 36, "TRK100006", [("BAG-004", 1)]),
    ("marcus@example.com", OrderStatus.cancelled, 20, None, None, [("LAMP-006", 1)]),
]


def seed() -> None:
    with SessionLocal() as db:
        # Wipe old data and restart IDs at 1, so every run gives identical data
        db.execute(text(
            "TRUNCATE order_items, orders, products, customers RESTART IDENTITY CASCADE"
        ))

        products = {
            sku: Product(sku=sku, name=name, category=category, price=Decimal(price))
            for sku, name, category, price in PRODUCTS
        }
        customers = {email: Customer(name=name, email=email) for name, email in CUSTOMERS}
        db.add_all([*products.values(), *customers.values()])

        for email, status, ordered, delivered, tracking, lines in ORDERS:
            items = [
                OrderItem(product=products[sku], quantity=qty, unit_price=products[sku].price)
                for sku, qty in lines
            ]
            db.add(Order(
                customer=customers[email],
                status=status,
                ordered_at=days_ago(ordered),
                delivered_at=days_ago(delivered) if delivered is not None else None,
                tracking_number=tracking,
                total_amount=sum(item.unit_price * item.quantity for item in items),
                items=items,
            ))

        db.commit()

    print(f"Seeded {len(CUSTOMERS)} customers, {len(PRODUCTS)} products, {len(ORDERS)} orders.")


if __name__ == "__main__":
    seed()