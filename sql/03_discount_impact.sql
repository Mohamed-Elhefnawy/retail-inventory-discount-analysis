-- Promotion families (region-specific copies grouped by name type) vs full-price lines.
SELECT CASE WHEN pr.discount_pct = 0 THEN 'No discount'
            ELSE regexp_replace(pr.promotion_name, '^(North America|European|Asian) ', '') || ' (' || round(100*pr.discount_pct)::INT || '% off)' END AS promo,
       count(*) AS lines, round(sum(s.net_sales)/1e6,1) AS net_sales_m,
       round(sum(s.qty)::DOUBLE/count(*),2) AS units_per_line,
       round(100*(sum(s.net_sales)-sum(s.total_cost))/sum(s.net_sales),2) AS gross_margin_pct,
       round(sum(s.discount_amt)/1e6,2) AS discount_given_m,
       round(100*sum(s.return_amt)/sum(s.gross_sales),2) AS return_pct
FROM sales s JOIN promotion pr USING (promotion_key) GROUP BY 1 ORDER BY net_sales_m DESC;
