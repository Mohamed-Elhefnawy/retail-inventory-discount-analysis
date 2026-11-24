SELECT year(sale_date) AS year,
       round(sum(net_sales)/1e6,1) AS net_sales_m, round(sum(total_cost)/1e6,1) AS cost_m,
       round(100*(sum(net_sales)-sum(total_cost))/sum(net_sales),2) AS gross_margin_pct,
       round(100*sum(discount_amt)/sum(gross_sales),2) AS discount_pct_of_gross,
       round(100*sum(return_amt)/sum(gross_sales),2) AS return_pct_of_gross,
       sum(qty) AS units
FROM sales GROUP BY 1 ORDER BY 1;
