-- Top products to reorder: urgent shortfall, ranked by weekly demand affected.
SELECT p.product_name, p.category, count(*) AS stores_urgent,
       sum(ip.safety_stock - ip.on_hand) AS units_short_of_safety,
       round(sum(ip.wk_units),1) AS weekly_units_demand,
       round(sum((ip.safety_stock - ip.on_hand) * ip.unit_cost)) AS cost_to_restore
FROM inv_position ip JOIN product p USING (product_key)
WHERE ip.below_safety_no_order = 1
GROUP BY 1,2 ORDER BY weekly_units_demand DESC LIMIT 25;
