-- Portfolio example using demonstration table names and fields.
-- It contains no employer or client sales data.

WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(s.quantity) AS units_sold,
        SUM(s.quantity * s.unit_price) AS revenue,
        SUM(s.quantity * s.unit_cost) AS cost_of_sales
    FROM sales AS s
    INNER JOIN products AS p
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name
),
product_targets AS (
    SELECT
        product_id,
        SUM(target_revenue) AS target_revenue
    FROM sales_targets
    GROUP BY product_id
)
SELECT
    ps.product_name,
    ps.units_sold,
    ROUND(ps.revenue, 2) AS revenue,
    ROUND(ps.cost_of_sales, 2) AS cost_of_sales,
    ROUND(ps.revenue - ps.cost_of_sales, 2) AS gross_profit,
    ROUND(100.0 * (ps.revenue - ps.cost_of_sales)
        / NULLIF(ps.revenue, 0), 2) AS gross_margin_percent,
    ROUND(COALESCE(pt.target_revenue, 0), 2) AS target_revenue,
    ROUND(ps.revenue - COALESCE(pt.target_revenue, 0), 2) AS target_variance,
    RANK() OVER (ORDER BY ps.revenue DESC) AS revenue_rank
FROM product_sales AS ps
LEFT JOIN product_targets AS pt
    ON pt.product_id = ps.product_id
ORDER BY revenue_rank, ps.product_name;
