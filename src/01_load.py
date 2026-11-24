"""Load Contoso Retail DW pipe-delimited extracts into DuckDB (data/contoso.duckdb)."""
import duckdb, sys, os
SRC = sys.argv[1]  # folder holding unpacked table folders
con = duckdb.connect("data/contoso.duckdb")
cols = {
 "FactSales": "SalesKey,DateKey,ChannelKey,StoreKey,ProductKey,PromotionKey,CurrencyKey,UnitCost,UnitPrice,SalesQuantity,ReturnQuantity,ReturnAmount,DiscountQuantity,DiscountAmount,TotalCost,SalesAmount,ETLLoadID,LoadDate,UpdateDate",
 "FactInventory": "InventoryKey,DateKey,StoreKey,ProductKey,CurrencyKey,OnHandQuantity,OnOrderQuantity,SafetyStockQuantity,UnitCost,DaysInStock,MinDayInStock,MaxDayInStock,Aging,ETLLoadID,LoadDate,UpdateDate",
 "DimProduct": "ProductKey,ProductLabel,ProductName,ProductDescription,ProductSubcategoryKey,Manufacturer,BrandName,ClassID,ClassName,StyleID,StyleName,ColorID,ColorName,Size,SizeRange,SizeUnitMeasureID,Weight,WeightUnitMeasureID,UnitOfMeasureID,UnitOfMeasureName,StockTypeID,StockTypeName,UnitCost,UnitPrice,AvailableForSaleDate,StopSaleDate,Status,ImageURL,ProductURL,ETLLoadID,LoadDate,UpdateDate",
 "DimProductSubcategory": "ProductSubcategoryKey,ProductSubcategoryLabel,ProductSubcategoryName,ProductSubcategoryDescription,ProductCategoryKey,ETLLoadID,LoadDate,UpdateDate",
 "DimProductCategory": "ProductCategoryKey,ProductCategoryLabel,ProductCategoryName,ProductCategoryDescription,ETLLoadID,LoadDate,UpdateDate",
 "DimStore": "StoreKey,GeographyKey,StoreManager,StoreType,StoreName,StoreDescription,Status,OpenDate,CloseDate,EntityKey,ZipCode,ZipCodeExtension,StorePhone,StoreFax,AddressLine1,AddressLine2,CloseReason,EmployeeCount,SellingAreaSize,LastRemodelDate,GeoLocation,Geometry,ETLLoadID,LoadDate,UpdateDate",
 "DimGeography": None,
 "DimPromotion": "PromotionKey,PromotionLabel,PromotionName,PromotionDescription,DiscountPercent,PromotionType,PromotionCategory,MinQuantity,MaxQuantity,StartDate,EndDate,ETLLoadID,LoadDate,UpdateDate",
 "DimChannel": "ChannelKey,ChannelLabel,ChannelName,ChannelDescription,ETLLoadID,LoadDate,UpdateDate",
}
for t, c in cols.items():
    if c is None: continue
    names = c.split(",")
    con.execute(f"DROP TABLE IF EXISTS {t}")
    con.execute(f"""CREATE TABLE {t} AS SELECT * FROM read_csv('{SRC}/{t}/*', delim='|', header=false,
        names={names}, all_varchar=true, quote='', escape='', null_padding=true, ignore_errors=true)""")
    print(t, con.execute(f"select count(*) from {t}").fetchone()[0])
