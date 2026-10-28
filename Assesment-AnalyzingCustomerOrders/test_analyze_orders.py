import unittest
from decimal import Decimal

from analyze_orders import CUSTOMERS, ORDERS, analyze_orders, render_report


class AnalyzeOrdersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis = analyze_orders(ORDERS, CUSTOMERS)

    def test_customer_spending_and_classifications(self) -> None:
        self.assertEqual(self.analysis["customer_spending"]["Alice"], Decimal("1029.97"))
        self.assertEqual(self.analysis["classifications"]["Alice"], "High-value buyer")
        self.assertEqual(self.analysis["classifications"]["Chloe"], "Moderate buyer")
        self.assertEqual(self.analysis["classifications"]["Frank"], "Low-value buyer")

    def test_category_revenue_and_customer_sets(self) -> None:
        self.assertEqual(
            self.analysis["category_revenue"]["Electronics"], Decimal("2558.96")
        )
        self.assertEqual(
            self.analysis["electronics_and_clothing_customers"],
            {"Bob", "David", "Eva"},
        )
        self.assertEqual(
            self.analysis["multi_category_customers"],
            {"Alice", "Bob", "David", "Eva", "Frank"},
        )

    def test_top_customers_and_product_frequency(self) -> None:
        self.assertEqual(
            [customer for customer, _ in self.analysis["top_customers"]],
            ["David", "Alice", "Eva"],
        )
        self.assertEqual(self.analysis["product_counts"]["Laptop"], 2)

    def test_classification_thresholds(self) -> None:
        orders = [
            ("At100", "P1", Decimal("100.00"), "Test"),
            ("At50", "P2", Decimal("50.00"), "Test"),
            ("Under50", "P3", Decimal("49.99"), "Test"),
            ("Over100", "P4", Decimal("100.01"), "Test"),
        ]
        analysis = analyze_orders(orders, ["At100", "At50", "Under50", "Over100"])
        self.assertEqual(analysis["classifications"]["At100"], "Moderate buyer")
        self.assertEqual(analysis["classifications"]["At50"], "Moderate buyer")
        self.assertEqual(analysis["classifications"]["Under50"], "Low-value buyer")
        self.assertEqual(analysis["classifications"]["Over100"], "High-value buyer")

    def test_report_contains_requested_sections(self) -> None:
        report = render_report(self.analysis)
        self.assertIn("Customer classification", report)
        self.assertIn("Product category analysis", report)
        self.assertIn("Business insights", report)


if __name__ == "__main__":
    unittest.main()
