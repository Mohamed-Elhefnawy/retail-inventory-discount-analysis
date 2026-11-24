SELECT p.category, round(sum(ip.stock_value)/1e6,2) AS stock_value_m,
       round(sum(CASE WHEN ip.cover_band IN ('Over 26 wks cover','No sales in 13 wks') THEN ip.stock_value END)/1e6,2) AS overstock_value_m,
       round(100*sum(CASE WHEN ip.cover_band IN ('Over 26 wks cover','No sales in 13 wks') THEN ip.stock_value END)/sum(ip.stock_value),1) AS overstock_pct
FROM inv_position ip JOIN product p USING (product_key) GROUP BY 1 ORDER BY overstock_value_m DESC;
