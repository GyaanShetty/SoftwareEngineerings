"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import os
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}


def place_table_order(table_id, guest, items_count, order_log=None):
    """Create a new order for a table; return False if invalid or taken."""
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {"guest": guest, "items": items_count, "bill": 15.0 * items_count, "is_settled": False}
    order_log.append(f"Created order for {table_id} with {items_count} dishes")
    return True


def void_table_order(table_id):
    """Remove a table's order; return False if it does not exist."""
    try:
        del orders[table_id]
    except KeyError:
        return False
    return True


def check_table_status(table_id):
    """Return True if the table has an unsettled (pending) order."""
    order = orders.get(table_id)
    if order is None:
        return False
    return not order["is_settled"]


def calculate_discounted_bill(table_id, discount_pct):
    """Apply a percentage discount (0-100) to a table's bill."""
    base_bill = orders[table_id]["bill"]
    pct = float(discount_pct)
    if not 0 <= pct <= 100:
        raise ValueError("discount must be between 0 and 100")
    return base_bill * (1 - pct / 100)


def generate_ticket_hash(table_id):
    """Return a SHA-256 hash identifying the kitchen ticket."""
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    """Return a cryptographically secure 4-digit POS PIN."""
    return secrets.randbelow(9000) + 1000


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Write current orders to a file for the kitchen printer."""
    with open(filename, "w", encoding="utf-8") as out:
        out.write(str(orders))
    print("Ticket sent to kitchen printer: " + filename)


def get_pending_summary(order_book):
    """Count orders that are not yet settled."""
    return sum(1 for d in order_book.values() if not d["is_settled"])


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = os.environ.get("POS_TERMINAL_KEY", "")
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    print("Discounted Bill:", calculate_discounted_bill("T1", 10))
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS Secret configured:", bool(pos_terminal_key))


main()