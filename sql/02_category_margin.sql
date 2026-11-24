SELECT p.category, round(sum(s.net_sales)/1e6,1) AS net_sales_m,
       round(100*(sum(s.net_sales)-sum(s.total_cost))/sum(s.net_sales),2) AS gross_margin_pct,
       round(100*sum(s.discount_amt)/sum(s.gross_sales),2) AS discount_pct,
       round(100*sum(s.return_amt)/sum(s.gross_sales),2) AS return_pct
FROM sales s JOIN product p USING (product_key) GROUP BY 1 ORDER BY net_sales_m DESC;
