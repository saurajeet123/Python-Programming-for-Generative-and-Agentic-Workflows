# Customer Order Analysis — Implementation Write-Up

## 1. Project purpose

This project demonstrates how core Python data structures and control
structures can be used to analyze a small e-commerce order dataset. It turns
sample customer orders into a report that summarizes customer spending,
spending classifications, category revenue, product popularity, and
cross-category purchasing behavior.

The dataset is illustrative and is defined directly in the project source.
The results describe only these sample orders; they should not be treated as
findings about a real customer base.

## 2. Implementation plan

The work is organized into the following steps:

1. **Represent the input data.** Define the customer list and store each order
   as a tuple containing customer, product, price, and category.
2. **Build convenient lookup structures.** Create a customer-to-products
   dictionary and derive product/category and category/customer mappings while
   processing orders.
3. **Calculate metrics in one pass.** Accumulate customer spending, category
   revenue, and product purchase counts from the order tuples.
4. **Classify and compare customers.** Apply the spending thresholds, sort
   customers by total spending, and use sets to find category overlap.
5. **Render the results.** Format the calculated values as a readable Markdown
   report, print it, and save it under the project’s `reports` directory.
6. **Verify expected behavior.** Use unit tests for representative totals,
   classification boundaries, set results, product frequency, top customers,
   and report sections.

## 3. Project structure

```text
Assesment-AnalyzingCustomerOrders/
├── analyze_orders.py
├── test_analyze_orders.py
├── README.md
├── IMPLEMENTATION.md
└── reports/
    └── customer_order_report.md
```

- `analyze_orders.py` contains the sample data, analysis functions, report
  rendering, and command-line entry point.
- `test_analyze_orders.py` contains the standard-library `unittest` suite.
- `README.md` gives basic setup, run, and test instructions.
- `IMPLEMENTATION.md` records the design and calculation details.
- `reports/customer_order_report.md` is the generated report; running the
  script again refreshes it from the source data.

## 4. Data model and Python concepts

### Input data

- `CUSTOMERS` is a list of six customer names.
- `ORDERS` is a list of 15 tuples. Each tuple has the shape
  `(customer_name, product, price, category)`.
- Prices use `Decimal` rather than binary floating-point numbers so that
  currency totals remain exact to the supplied decimal values.
- The `Order` type alias documents the order tuple shape. The `Analysis`
  `TypedDict` describes the structured results returned by the analysis.

The sample contains three categories: Electronics, Clothing, and Home
Essentials.

### Derived structures

The analysis uses:

- Dictionaries for customer spending, customer products, product categories,
  category revenue, customer classifications, and customers per category.
- Sets for distinct categories, distinct products, customers in each category,
  and customers who purchased across categories.
- A `Counter` to count how often each product appears in the order list.
- Lists for the ordered customer input, customer product histories, and the
  electronics customer result.
- Loops to accumulate totals and category membership; a list comprehension
  selects customers who bought Electronics.
- Sorting to rank top spenders and to make report ordering predictable.

`build_customer_products` initializes a product list for each known customer
and uses `setdefault` to support a customer encountered in the orders even if
they were not initially listed.

## 5. Analysis and business rules

### Customer spending classification

Every order price is added to its customer's running total. Each listed price
is treated as the amount contributed by that order record; the input format
does not include a separate quantity or order identifier.

Classification uses these inclusive/exclusive boundaries:

| Total spending | Classification |
|---|---|
| More than $100.00 | High-value buyer |
| $50.00 through $100.00 inclusive | Moderate buyer |
| Less than $50.00 | Low-value buyer |

Customers supplied in `CUSTOMERS` with no orders would still receive a
zero-spending total and be classified as low-value.

### Product and category analysis

For each order, the script:

1. Associates the product with the order's category.
2. Adds the price to that category's revenue.
3. Records the customer as a member of that category's customer set.
4. Increments the product's purchase count.

Unique products are extracted from the product-count keys. The available
categories are derived from categories that appear in the order data. The
electronics customer list is selected from each customer's product history by
checking the product-to-category mapping.

### Customer intersections and ranking

- A customer is considered to have purchased from multiple categories when
  their set of distinct categories has more than one member.
- Customers who purchased both Electronics and Clothing are found by
  intersecting those two category customer sets.
- The top three customers are sorted by descending spending. Customer name is
  used as a stable alphabetical tie-breaker.
- All products tied for the highest purchase count are reported as most
  frequently purchased.

## 6. Report generation

`render_report` formats the analysis as Markdown, including:

- A per-customer spending and classification table.
- The available categories and revenue per category, sorted by revenue.
- Unique products, most frequently purchased products, electronics buyers,
  top spenders, and cross-category customer groups.
- Short business observations based on the category revenue and top customer.

`main` runs the analysis over the sample dataset, creates `reports/` if it is
missing, writes the report as UTF-8, and prints both the report and its output
path. No third-party packages or external files are required.

## 7. Sample results

For the included dataset:

- Total sample revenue is **$2,985.94**.
- Electronics has the highest category revenue at **$2,558.96**; Clothing
  contributes **$245.00** and Home Essentials **$181.98**.
- David is the highest spender at **$1,054.99**, followed by Alice at
  **$1,029.97** and Eva at **$624.00**.
- Alice, Bob, David, and Eva purchased Electronics.
- Bob, David, and Eva purchased both Electronics and Clothing.
- Five products tie as the most frequently purchased, with two appearances
  each: Coffee Maker, Desk Lamp, Headphones, Laptop, and T-shirt.
- Alice, Bob, David, Eva, and Frank purchased from multiple categories.

The report suggests monitoring Electronics inventory, considering retention
offers for the highest-value customers, and reviewing frequently purchased
items for replenishment or cross-selling opportunities. These are exploratory
suggestions based on a deliberately small sample, not statistically
representative recommendations.

## 8. Validation

Run the test suite from the project directory:

```powershell
python -m unittest -v
```

The five tests verify:

1. A sample customer's spending and one example of each buyer classification.
2. Electronics category revenue and the expected category-customer set
   intersections.
3. Top-customer ordering and a repeated product count.
4. All four classification boundary cases: $49.99, $50.00, $100.00, and
   $100.01.
5. Presence of the customer, category, and business-insight sections in the
   rendered report.

Run the analysis and regenerate the report with:

```powershell
python analyze_orders.py
```

## 9. Assumptions and limitations

- The data is static sample data embedded in Python; there is no CSV, database,
  web service, or live store integration.
- Each tuple is one order record and contributes its listed price once. The
  format does not represent quantity, discounts, tax, shipping, refunds, or
  timestamps.
- The product-to-category dictionary is derived from the tuples. A product is
  expected to have a consistent category across all its records.
- Revenue is the sum of listed order prices, not a profit calculation. Cost
  data is not provided, so category profitability cannot be measured.
- The report describes a small sample. Larger or real-world datasets would
  need validation for malformed records, duplicate order IDs, inconsistent
  customer/product naming, and possibly an external data source.
