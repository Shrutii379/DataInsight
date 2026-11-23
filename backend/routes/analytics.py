
from fastapi import APIRouter
from sqlalchemy import text
from backend.database import engine

router = APIRouter()


# 1. KPI API
@router.get("/kpis")
def get_kpis():

    query = text("""
        SELECT
            COALESCE(SUM("TotalSales"), 0) AS total_revenue,
            COUNT(DISTINCT "Invoice") AS total_orders,
            COUNT(DISTINCT "Customer ID") AS total_customers,
            COUNT(DISTINCT "StockCode") AS total_products
        FROM ecommerce_sales
        WHERE "Quantity" > 0
          AND "Price" > 0
          AND CAST("Invoice" AS TEXT) NOT LIKE 'C%'
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    return dict(result)


# 2. Monthly Revenue API
@router.get("/monthly-revenue")
def get_monthly_revenue():

    query = text("""
        SELECT
            "Year",
            "Month",
            "MonthName",
            SUM("TotalSales") AS revenue
        FROM ecommerce_sales
        WHERE "Quantity" > 0
          AND "Price" > 0
        GROUP BY "Year", "Month", "MonthName"
        ORDER BY "Year", "Month"
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# 3. Top 10 Products API
@router.get("/top-products")
def get_top_products():

    query = text("""
        SELECT
            "StockCode",
            "Description",
            SUM("Quantity") AS total_quantity,
            SUM("TotalSales") AS total_revenue
        FROM ecommerce_sales
        WHERE "Quantity" > 0
          AND "Price" > 0
        GROUP BY "StockCode", "Description"
        ORDER BY total_revenue DESC
        LIMIT 10
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# 4. Country-wise Revenue API
@router.get("/top-countries")
def get_top_countries():

    query = text("""
        SELECT
            "Country",
            COUNT(DISTINCT "Invoice") AS total_orders,
            SUM("Quantity") AS total_quantity,
            SUM("TotalSales") AS total_revenue
        FROM ecommerce_sales
        WHERE "Quantity" > 0
          AND "Price" > 0
        GROUP BY "Country"
        ORDER BY total_revenue DESC
        LIMIT 10
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# 5. Customer Analysis API
@router.get("/customer-analysis")
def get_customer_analysis():

    query = text("""
        SELECT
            "Customer ID",
            COUNT(DISTINCT "Invoice") AS total_orders,
            SUM("TotalSales") AS total_revenue,
            SUM("Quantity") AS total_quantity
        FROM ecommerce_sales
        WHERE "Quantity" > 0
          AND "Price" > 0
          AND "Customer ID" IS NOT NULL
        GROUP BY "Customer ID"
        ORDER BY total_revenue DESC
        LIMIT 10
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# 6. Filter Options API
@router.get("/filter-options")
def get_filter_options():

    query = text("""
        SELECT
            ARRAY(
                SELECT DISTINCT "Year"
                FROM ecommerce_sales
                WHERE "Year" IS NOT NULL
                ORDER BY "Year"
            ) AS years,

            ARRAY(
                SELECT DISTINCT "Country"
                FROM ecommerce_sales
                WHERE "Country" IS NOT NULL
                ORDER BY "Country"
            ) AS countries
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    return dict(result)


# 7. Filtered Dashboard API
@router.get("/dashboard-data")
def get_dashboard_data(year: int | None = None, country: str | None = None):

    filters = """
        "Quantity" > 0
        AND "Price" > 0
        AND (:year IS NULL OR "Year" = :year)
        AND (:country IS NULL OR "Country" = :country)
    """

    params = {
        "year": year,
        "country": country
    }

    with engine.connect() as connection:

        # KPI Data
        kpi_query = text(f"""
            SELECT
                COALESCE(SUM("TotalSales"), 0) AS total_revenue,
                COUNT(DISTINCT "Invoice") AS total_orders,
                COUNT(DISTINCT "Customer ID") AS total_customers,
                COUNT(DISTINCT "StockCode") AS total_products
            FROM ecommerce_sales
            WHERE {filters}
        """)

        kpis = dict(
            connection.execute(
                kpi_query, params
            ).mappings().first()
        )

        # Monthly Revenue
        monthly_query = text(f"""
            SELECT
                "Year",
                "Month",
                "MonthName",
                SUM("TotalSales") AS revenue
            FROM ecommerce_sales
            WHERE {filters}
            GROUP BY "Year", "Month", "MonthName"
            ORDER BY "Year", "Month"
        """)

        monthly = [
            dict(row) for row in
            connection.execute(
                monthly_query, params
            ).mappings().all()
        ]

        # Top Products
        products_query = text(f"""
            SELECT
                "StockCode",
                "Description",
                SUM("Quantity") AS total_quantity,
                SUM("TotalSales") AS total_revenue
            FROM ecommerce_sales
            WHERE {filters}
            GROUP BY "StockCode", "Description"
            ORDER BY total_revenue DESC
            LIMIT 10
        """)

        products = [
            dict(row) for row in
            connection.execute(
                products_query, params
            ).mappings().all()
        ]

        # Top Countries
        countries_query = text(f"""
            SELECT
                "Country",
                COUNT(DISTINCT "Invoice") AS total_orders,
                SUM("Quantity") AS total_quantity,
                SUM("TotalSales") AS total_revenue
            FROM ecommerce_sales
            WHERE {filters}
            GROUP BY "Country"
            ORDER BY total_revenue DESC
            LIMIT 10
        """)

        countries = [
            dict(row) for row in
            connection.execute(
                countries_query, params
            ).mappings().all()
        ]

        # Customer Analysis
        customers_query = text(f"""
            SELECT
                "Customer ID",
                COUNT(DISTINCT "Invoice") AS total_orders,
                SUM("TotalSales") AS total_revenue,
                SUM("Quantity") AS total_quantity
            FROM ecommerce_sales
            WHERE {filters}
              AND "Customer ID" IS NOT NULL
            GROUP BY "Customer ID"
            ORDER BY total_revenue DESC
            LIMIT 10
        """)

        customers = [
            dict(row) for row in
            connection.execute(
                customers_query, params
            ).mappings().all()
        ]

        # 8. Average Order Value (AOV)
        aov_query = text(f"""
            SELECT
                COALESCE(
                    SUM("TotalSales") /
                    NULLIF(COUNT(DISTINCT "Invoice"), 0),
                    0
                ) AS average_order_value
            FROM ecommerce_sales
            WHERE {filters}
        """)

        aov = connection.execute(
            aov_query, params
        ).mappings().first()

        # 9. Repeat Customers
        repeat_query = text(f"""
            SELECT
                COUNT(*) AS repeat_customers
            FROM (
                SELECT "Customer ID"
                FROM ecommerce_sales
                WHERE {filters}
                  AND "Customer ID" IS NOT NULL
                GROUP BY "Customer ID"
                HAVING COUNT(DISTINCT "Invoice") > 1
            ) AS repeat_customer_data
        """)

        repeat_customers = connection.execute(
            repeat_query, params
        ).scalar()

        # 10. Repeat Purchase Rate
        total_customers = kpis["total_customers"]

        repeat_purchase_rate = (
            (repeat_customers / total_customers) * 100
            if total_customers > 0
            else 0
        )

    # Return Dashboard Data
    return {
        "kpis": kpis,
        "average_order_value": aov["average_order_value"],
        "repeat_customers": repeat_customers,
        "repeat_purchase_rate": repeat_purchase_rate,
        "monthly_revenue": monthly,
        "top_products": products,
        "top_countries": countries,
        "customer_analysis": customers
    }
