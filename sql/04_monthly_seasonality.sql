SELECT date_trunc('month', sale_date)::DATE AS month, round(sum(net_sales)/1e6,1) AS net_sales_m,
       round(100*(sum(net_sales)-sum(total_cost))/sum(net_sales),2) AS gross_margin_pct,
       round(100*sum(discount_amt)/sum(gross_sales),2) AS discount_pct
FROM sales GROUP BY 1 ORDER BY 1;
