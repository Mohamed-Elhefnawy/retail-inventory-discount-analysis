-- Categories where stock sits below safety stock with nothing on order, weighted by demand.
SELECT p.category, count(*) AS store_products,
       sum(ip.below_safety) AS below_safety, sum(ip.below_safety_no_order) AS below_safety_no_order,
       round(100.0*sum(ip.below_safety_no_order)/count(*),1) AS pct_urgent,
       round(sum(CASE WHEN ip.below_safety_no_order=1 THEN ip.wk_units END),0) AS weekly_units_at_risk
FROM inv_position ip JOIN product p USING (product_key) GROUP BY 1 ORDER BY pct_urgent DESC;
