import os
import json
import re
from modules.revenue.badge_model import estimate_from_badge
from modules.revenue.review_model import estimate_from_reviews


class RevenueEngine:

    def __init__(self, company_path):
        self.company_path = company_path
        self.products_path = os.path.join(company_path, "products")
        self.revenue_path = os.path.join(company_path, "revenue")
        os.makedirs(self.revenue_path, exist_ok=True)

    # ---------------------------------------
    # Extract numeric price from string
    # ---------------------------------------
    def extract_price_number(self, price_text):

        if not price_text:
            return 0

        match = re.search(r"[\d,]+", str(price_text))
        if not match:
            return 0

        return int(match.group().replace(",", ""))

    # ---------------------------------------
    # Process individual platform
    # ---------------------------------------
    def process_platform(self, platform_name):

        platform_folder = os.path.join(self.products_path, platform_name)

        if not os.path.isdir(platform_folder):
            print(f"[Revenue] Platform folder not found: {platform_name}")
            return None

        platform_file = os.path.join(
            platform_folder,
            f"{platform_name}_products.json"
        )

        if not os.path.exists(platform_file):
            print(f"[Revenue] No product file for {platform_name}")
            return None

        with open(platform_file, "r") as f:
            products = json.load(f)

        if not products:
            print(f"[Revenue] No products scraped for {platform_name}")
            return None

        enriched_products = []
        total_monthly_revenue = 0
        total_yearly_revenue = 0

        for product in products:

            price = self.extract_price_number(product.get("price"))
            badge_raw = product.get("bought_last_month_raw")

            # Estimate monthly units
            if badge_raw:
                monthly_units = estimate_from_badge(badge_raw)
            else:
                monthly_units = estimate_from_reviews(
                    product.get("review_count")
                )

            yearly_units = monthly_units * 12
            monthly_revenue = monthly_units * price
            yearly_revenue = yearly_units * price

            product["estimated_monthly_units"] = monthly_units
            product["estimated_yearly_units"] = yearly_units
            product["estimated_monthly_revenue"] = monthly_revenue
            product["estimated_yearly_revenue"] = yearly_revenue

            total_monthly_revenue += monthly_revenue
            total_yearly_revenue += yearly_revenue

            enriched_products.append(product)

        # Save detailed revenue file
        enriched_file = os.path.join(
            self.revenue_path,
            f"{platform_name}_revenue_analysis.json"
        )

        with open(enriched_file, "w") as f:
            json.dump(enriched_products, f, indent=4)

        # Save platform summary
        summary = {
            "platform": platform_name,
            "total_products": len(enriched_products),
            "estimated_total_monthly_revenue": total_monthly_revenue,
            "estimated_total_yearly_revenue": total_yearly_revenue
        }

        summary_file = os.path.join(
            self.revenue_path,
            f"{platform_name}_summary.json"
        )

        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=4)

        print(f"[Revenue] {platform_name} revenue processed.")

        return summary

    # ---------------------------------------
    # Run revenue engine
    # ---------------------------------------
    def run(self):

        if not os.path.isdir(self.products_path):
            print("[Revenue] No products directory found.")
            return None

        platform_summaries = []

        for platform_name in os.listdir(self.products_path):

            platform_folder = os.path.join(self.products_path, platform_name)

            # Skip non-directories
            if not os.path.isdir(platform_folder):
                continue

            summary = self.process_platform(platform_name)

            if summary:
                platform_summaries.append(summary)

        if not platform_summaries:
            print("[Revenue] No platform revenue generated.")
            return None

        # Aggregate overall revenue
        grand_monthly = sum(
            p["estimated_total_monthly_revenue"]
            for p in platform_summaries
        )

        grand_yearly = sum(
            p["estimated_total_yearly_revenue"]
            for p in platform_summaries
        )

        overall_summary = {
            "total_platforms": len(platform_summaries),
            "estimated_combined_monthly_revenue": grand_monthly,
            "estimated_combined_yearly_revenue": grand_yearly
        }

        overall_file = os.path.join(
            self.revenue_path,
            "overall_summary.json"
        )

        with open(overall_file, "w") as f:
            json.dump(overall_summary, f, indent=4)

        print("[Revenue] Overall revenue aggregation completed.")

        return overall_summary