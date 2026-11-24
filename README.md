# Contoso Retail: Inventory, Discount and Margin Analysis

SQL and Python analysis of a retail sales and inventory warehouse: which products to reorder, where stock is tied up, and what promotions do to margin.

**Dashboard:** open `docs/index.html` (interactive charts, no setup needed). Static previews are in `screenshots/`.

## About the data

Microsoft's **Contoso Retail Data Warehouse**, a fictitious retailer used for BI demos: 3.4M sales lines (2007 to 2009), 8.0M weekly inventory records, 306 stores, about 2,500 products. The fields are realistic (unit cost, discount amount, return amount, on-hand, on-order, safety stock), but the records are synthetic. The results show the method, not the performance of a real business. Amounts are in the dataset's own currency units.

Sources: [Microsoft Contoso BI Demo Dataset](https://www.microsoft.com/en-us/download/details.aspx?id=18279) and Microsoft's [contoso-data-warehouse sample](https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/contoso-data-warehouse) (MIT-licensed sample repository). `src/00_download.sh` downloads the tables from a public mirror of the same files. Raw data is not stored in this repository.

## Questions

1. Which products and categories need reordering now?
2. Where is inventory capital tied up in slow-moving stock?
3. How do promotions change margin and volume?
4. How do margin, discounts and returns vary by category and season?

## Findings

- **Discounts cost margin and do not always buy volume.** Full-price lines earn 57.6% gross margin. The Spring 20% promotion earns 55.5% and sells 14.6 units per line against 14.8 at full price. The Holiday 15% promotion sells 20.9 units per line at 56.0% margin. Promotions run in specific seasons and regions, so this is an association, not a proven effect.
- **37% of stock value is overstock.** 28.7M of 78.5M sits in store-products with more than 26 weeks of cover. Home Appliances (9.3M) and Computers (8.2M) hold the most.
- **Shortages are concentrated.** 12.3% of store-products are below safety stock with nothing on order. In Music, Movies and Audio Books it is 67%. Cell phone accessories carry the largest weekly demand at risk (about 4,300 units per week).
- **Sales fell while units rose.** Net sales dropped from 4.56B (2007) to 3.74B (2009) while units sold rose from 17.0M to 19.8M. Revenue per unit fell about 30% and gross margin stayed near 57%. The data cannot separate lower prices from a shift to cheaper products.
- **Margin by category** ranges from 53.8% (Games and Toys) to 60.8% (Music, Movies and Audio Books).

## Method

| Step | File |
|---|---|
| Load pipe-delimited tables into DuckDB | `src/01_load.py` |
| Typed views, KPIs, category margin, promotion impact, seasonality | `sql/00` to `sql/04` |
| Inventory position at the latest weekly snapshot (26 Dec 2009) joined to trailing 13-week unit sales | `sql/05` |
| Reorder risk, top reorder list, overstock by category | `sql/06` to `sql/08` |
| Build the dashboard | `src/03_dashboard.py` |

Definitions:

- **Weeks of cover** = on-hand units at the latest snapshot divided by average weekly units sold over the trailing 13 weeks, per store and product.
- **Overstock** = more than 26 weeks of cover, or on hand with no sales in 13 weeks.
- **Urgent reorder** = on-hand below safety stock with zero on order.
- **Gross margin** = (net sales minus total cost) divided by net sales. **Discount rate** = discount amount divided by gross sales (quantity times unit price).

## Limitations

- Synthetic data: no real customers, prices or stock.
- Gross margin uses the dataset's unit cost and excludes operating costs.
- Inventory is weekly, sales are daily; cover uses a 13-week window and does not model seasonality or lead times.
- Promotion comparison is observational and not adjusted for season, region or product mix.

## Run it

```bash
pip install -r requirements.txt
./run_all.sh
```

Results are written to `results/*.csv` and the dashboard to `docs/index.html`.
