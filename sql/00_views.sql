-- Typed views over the raw (all-varchar) load.
CREATE OR REPLACE VIEW sales AS
SELECT CAST(s.DateKey AS DATE) AS sale_date, CAST(s.StoreKey AS INT) AS store_key, CAST(s.ProductKey AS INT) AS product_key,
       CAST(s.PromotionKey AS INT) AS promotion_key, CAST(s.ChannelKey AS INT) AS channel_key,
       CAST(s.SalesQuantity AS INT) AS qty, CAST(s.ReturnQuantity AS INT) AS return_qty,
       CAST(s.UnitPrice AS DOUBLE) AS unit_price, CAST(s.UnitCost AS DOUBLE) AS unit_cost,
       CAST(s.SalesAmount AS DOUBLE) AS net_sales, CAST(s.TotalCost AS DOUBLE) AS total_cost,
       CAST(s.DiscountAmount AS DOUBLE) AS discount_amt, CAST(s.ReturnAmount AS DOUBLE) AS return_amt,
       CAST(s.SalesQuantity AS INT) * CAST(s.UnitPrice AS DOUBLE) AS gross_sales
FROM FactSales s;

CREATE OR REPLACE VIEW inventory AS
SELECT CAST(DateKey AS DATE) AS snap_date, CAST(StoreKey AS INT) AS store_key, CAST(ProductKey AS INT) AS product_key,
       CAST(OnHandQuantity AS INT) AS on_hand, CAST(OnOrderQuantity AS INT) AS on_order,
       CAST(SafetyStockQuantity AS INT) AS safety_stock, CAST(UnitCost AS DOUBLE) AS unit_cost,
       CAST(DaysInStock AS INT) AS days_in_stock, CAST(Aging AS INT) AS aging
FROM FactInventory;

CREATE OR REPLACE VIEW product AS
SELECT CAST(p.ProductKey AS INT) AS product_key, p.ProductName AS product_name, p.BrandName AS brand,
       sc.ProductSubcategoryName AS subcategory, trim(c.ProductCategoryName) AS category
FROM DimProduct p
LEFT JOIN DimProductSubcategory sc ON sc.ProductSubcategoryKey = p.ProductSubcategoryKey
LEFT JOIN DimProductCategory c ON c.ProductCategoryKey = sc.ProductCategoryKey;

CREATE OR REPLACE VIEW promotion AS
SELECT CAST(PromotionKey AS INT) AS promotion_key, regexp_replace(PromotionName, 'Scholl', 'School') AS promotion_name,
       CAST(DiscountPercent AS DOUBLE) AS discount_pct, PromotionType AS promo_type
FROM DimPromotion;
