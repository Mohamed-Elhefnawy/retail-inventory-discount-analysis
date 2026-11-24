-- Latest weekly snapshot, store x product, joined to trailing-13-week unit velocity.
CREATE OR REPLACE TABLE inv_position AS
WITH latest AS (SELECT max(snap_date) AS d FROM inventory),
vel AS (
  SELECT store_key, product_key, sum(qty)/13.0 AS wk_units
  FROM sales JOIN latest ON sale_date > latest.d - INTERVAL 91 DAY AND sale_date <= latest.d
  GROUP BY 1,2)
SELECT i.store_key, i.product_key, i.on_hand, i.on_order, i.safety_stock, i.unit_cost, i.aging,
       i.on_hand*i.unit_cost AS stock_value, coalesce(v.wk_units,0) AS wk_units,
       CASE WHEN i.on_hand < i.safety_stock THEN 1 ELSE 0 END AS below_safety,
       CASE WHEN i.on_hand < i.safety_stock AND i.on_order = 0 THEN 1 ELSE 0 END AS below_safety_no_order,
       CASE WHEN coalesce(v.wk_units,0) = 0 AND i.on_hand > 0 THEN 'No sales in 13 wks'
            WHEN i.on_hand / v.wk_units > 26 THEN 'Over 26 wks cover'
            WHEN i.on_hand / v.wk_units > 13 THEN '13-26 wks cover'
            ELSE 'Under 13 wks cover' END AS cover_band
FROM inventory i JOIN latest l ON i.snap_date = l.d
LEFT JOIN vel v ON v.store_key=i.store_key AND v.product_key=i.product_key;

SELECT cover_band, count(*) AS store_products, round(sum(stock_value)/1e6,2) AS stock_value_m,
       round(100*sum(stock_value)/sum(sum(stock_value)) OVER (),1) AS pct_of_value
FROM inv_position GROUP BY 1 ORDER BY stock_value_m DESC;
