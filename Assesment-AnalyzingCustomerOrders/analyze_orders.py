"""Analyze a sample of customer orders and generate a business report."""

from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import TypeAlias, TypedDict

Order: TypeAlias = tuple[str, str, Decimal, str]


class Analysis(TypedDict):
    category_by_product: dict[str, str]
    categories: set[str]
    category_revenue: dict[str, Decimal]
    customer_spending: dict[str, Decimal]
    classifications: dict[str, str]
    product_counts: Counter[str]
    unique_products: set[str]
    electronics_customers: list[str]
    top_customers: list[tuple[str, Decimal]]
    multi_category_customers: set[str]
    electronics_and_clothing_customers: set[str]
    customer_products: dict[str, list[str]]


CUSTOMERS = ["Alice", "Bob", "Chloe", "David", "Eva", "Frank"]

ORDERS: list[Order] = [
    ("Alice", "Laptop", Decimal("899.99"), "Electronics"),
    ("Alice", "Headphones", Decimal("79.99"), "Electronics"),
    ("Alice", "Coffee Maker", Decimal("49.99"), "Home Essentials"),
    ("Bob", "T-shirt", Decimal("25.00"), "Clothing"),
    ("Bob", "Jeans", Decimal("60.00"), "Clothing"),
    ("Bob", "Headphones", Decimal("79.99"), "Electronics"),
    ("Chloe", "Desk Lamp", Decimal("35.00"), "Home Essentials"),
    ("Chloe", "Coffee Maker", Decimal("49.99"), "Home Essentials"),
    ("David", "Laptop", Decimal("899.99"), "Electronics"),
    ("David", "Jacket", Decimal("120.00"), "Clothing"),
    ("David", "Desk Lamp", Decimal("35.00"), "Home Essentials"),
    ("Eva", "Smartphone", Decimal("599.00"), "Electronics"),
    ("Eva", "T-shirt", Decimal("25.00"), "Clothing"),
    ("Frank", "Socks", Decimal("15.00"), "Clothing"),
    ("Frank", "Mug", Decimal("12.00"), "Home Essentials"),
]


def build_customer_products(customers: list[str], orders: list[Order]) -> dict[str, list[str]]:
    """Build a customer-to-products lookup using dictionary methods."""
    customer_products = {customer: [] for customer in customers}
    for customer, product, _, _ in orders:
        customer_products.setdefault(customer, []).append(product)
    return customer_products


def analyze_orders(orders: list[Order], customers: list[str]) -> Analysis:
    """Calculate customer, category, and product insights from order tuples."""
    category_by_product: dict[str, str] = {}
    category_revenue: dict[str, Decimal] = {}
    category_customers: dict[str, set[str]] = {}
    customer_spending = dict.fromkeys(customers, Decimal("0.00"))
    product_counts: Counter[str] = Counter()
    customer_products = build_customer_products(customers, orders)

    for customer, product, price, category in orders:
        category_by_product[product] = category
        category_revenue[category] = category_revenue.get(category, Decimal("0.00")) + price
        category_customers.setdefault(category, set()).add(customer)
        customer_spending[customer] = customer_spending.get(customer, Decimal("0.00")) + price
        product_counts[product] += 1

    customer_categories: dict[str, set[str]] = {customer: set() for customer in customer_spending}
    for customer, _, _, category in orders:
        customer_categories.setdefault(customer, set()).add(category)

    classifications = {
        customer: (
            "High-value buyer"
            if total > Decimal("100.00")
            else "Moderate buyer"
            if total >= Decimal("50.00")
            else "Low-value buyer"
        )
        for customer, total in customer_spending.items()
    }
    electronics_customers = [
        customer
        for customer in customers
        if any(
            category_by_product[product] == "Electronics"
            for product in customer_products[customer]
        )
    ]
    top_customers = sorted(
        customer_spending.items(), key=lambda item: (-item[1], item[0])
    )[:3]
    multi_category_customers = {
        customer for customer, categories in customer_categories.items() if len(categories) > 1
    }
    electronics_buyers = category_customers.get("Electronics", set())
    clothing_buyers = category_customers.get("Clothing", set())

    return {
        "category_by_product": category_by_product,
        "categories": set(category_revenue),
        "category_revenue": category_revenue,
        "customer_spending": customer_spending,
        "classifications": classifications,
        "product_counts": product_counts,
        "unique_products": set(product_counts),
        "electronics_customers": electronics_customers,
        "top_customers": top_customers,
        "multi_category_customers": multi_category_customers,
        "electronics_and_clothing_customers": electronics_buyers & clothing_buyers,
        "customer_products": customer_products,
    }


def format_currency(amount: Decimal) -> str:
    return f"${amount:,.2f}"


def render_report(analysis: Analysis) -> str:
    """Render analysis results as a readable Markdown business report."""
    category_revenue = analysis["category_revenue"]
    customer_spending = analysis["customer_spending"]
    classifications = analysis["classifications"]
    product_counts = analysis["product_counts"]

    lines = [
        "# Customer Order Analysis",
        "",
        "## Customer classification",
        "",
        "| Customer | Total spending | Classification |",
        "|---|---:|---|",
    ]
    for customer in sorted(customer_spending):
        lines.append(
            f"| {customer} | {format_currency(customer_spending[customer])} "
            f"| {classifications[customer]} |"
        )

    lines.extend(["", "## Product category analysis", ""])
    lines.append("Available categories: " + ", ".join(sorted(analysis["categories"])))
    lines.extend(["", "| Category | Revenue |", "|---|---:|"])
    for category, revenue in sorted(
        category_revenue.items(), key=lambda item: (-item[1], item[0])
    ):
        lines.append(f"| {category} | {format_currency(revenue)} |")

    lines.extend(
        [
            "",
            "## Product and customer insights",
            "",
            f"- Unique products: {', '.join(sorted(analysis['unique_products']))}",
            "- Most frequently purchased products: "
            + ", ".join(
                f"{product} ({count} orders)"
                for product, count in sorted(
                    product_counts.items(), key=lambda item: (-item[1], item[0])
                )
                if count == max(product_counts.values())
            ),
            "- Customers who purchased Electronics: "
            + ", ".join(analysis["electronics_customers"]),
            "- Top three customers by spending: "
            + "; ".join(
                f"{customer} ({format_currency(total)})"
                for customer, total in analysis["top_customers"]
            ),
            "- Customers purchasing from multiple categories: "
            + ", ".join(sorted(analysis["multi_category_customers"])),
            "- Customers purchasing both Electronics and Clothing: "
            + ", ".join(sorted(analysis["electronics_and_clothing_customers"])),
            "",
            "## Business insights",
            "",
        ]
    )

    highest_category = max(category_revenue, key=category_revenue.get)
    top_customer, top_total = analysis["top_customers"][0]
    lines.extend(
        [
            f"- **{highest_category}** generated the highest category revenue "
            f"({format_currency(category_revenue[highest_category])}); prioritize "
            "stock availability and category-specific promotions there.",
            f"- **{top_customer}** is the highest spender at {format_currency(top_total)} "
            "and is a high-value buyer; consider retention or loyalty offers.",
            "- Frequently purchased products are candidates for replenishment planning "
            "and cross-selling.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    analysis = analyze_orders(ORDERS, CUSTOMERS)
    report = render_report(analysis)
    report_path = Path(__file__).parent / "reports" / "customer_order_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
