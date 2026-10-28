# Customer Order Analysis

A small, dependency-free Python project that demonstrates how lists, tuples,
dictionaries, sets, loops, conditionals, sorting, and a list comprehension can
be used to analyze e-commerce orders.

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for the implementation plan, data
model, analysis rules, sample findings, and limitations.

## Run

Use Python 3.10 or newer:

```powershell
python analyze_orders.py
```

The script prints the report and saves a Markdown copy to
`reports/customer_order_report.md`. The sample orders are defined as tuples in
`analyze_orders.py`, with prices represented as `Decimal` values to keep
currency totals exact.

## Test

```powershell
python -m unittest -v
```

## Analysis included

- Customer spending totals and buyer classifications: high-value is over $100,
  moderate is $50 through $100 inclusive, and low-value is below $50.
- Category revenue, available categories, unique products, and product
  purchase frequency.
- Electronics customers, the three highest-spending customers, customers who
  purchased across multiple categories, and customers who purchased both
  Electronics and Clothing.
- Business observations based on the calculated category revenue and customer
  spending.
