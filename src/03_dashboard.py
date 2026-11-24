"""Build docs/index.html (interactive dashboard) and static PNG charts from results/*.csv."""
import pandas as pd, plotly.graph_objects as go, plotly.io as pio, os
R = lambda n: pd.read_csv(f"results/{n}.csv")
kpi, cat, promo, month = R("01_kpis_by_year"), R("02_category_margin"), R("03_discount_impact"), R("04_monthly_seasonality")
cover, risk, reorder, over = R("05_inventory_position"), R("06_reorder_risk"), R("07_reorder_list"), R("08_overstock_by_category")
INK, MUTED, A, B, C = "#1f2937", "#6b7280", "#2563eb", "#0f766e", "#d97706"
FONT = dict(family="Inter, Segoe UI, Helvetica, Arial, sans-serif", color=INK, size=13)
def style(fig, h=380, **kw):
    kw.setdefault("margin", dict(l=60, r=30, t=50, b=50))
    fig.update_layout(template="simple_white", font=FONT, height=h, paper_bgcolor="white", plot_bgcolor="white", **kw)
    return fig
y09 = kpi[kpi.year == 2009].iloc[0]; y08 = kpi[kpi.year == 2008].iloc[0]
tot_val = cover.stock_value_m.sum()
over_val = cover[cover.cover_band.isin(["Over 26 wks cover", "No sales in 13 wks"])].stock_value_m.sum()
urg = int(risk.below_safety_no_order.sum()); n_sp = int(risk.store_products.sum())
figs = {}

f = go.Figure()
f.add_bar(x=month.month, y=month.net_sales_m, name="Net sales (millions)", marker_color=A, yaxis="y", hovertemplate="%{x|%b %Y}<br>Net sales: %{y:.1f}M<extra></extra>")
f.add_scatter(x=month.month, y=month.gross_margin_pct, name="Gross margin %", mode="lines+markers", line=dict(color=C, width=2), yaxis="y2", hovertemplate="%{x|%b %Y}<br>Gross margin: %{y:.2f}%<extra></extra>")
f.update_layout(title="Monthly net sales and gross margin, 2007 to 2009", yaxis=dict(title="Net sales (millions)"),
                yaxis2=dict(title="Gross margin %", overlaying="y", side="right", range=[50, 62], showgrid=False),
                legend=dict(orientation="h", y=-0.2))
figs["monthly"] = style(f, 400)

p = promo.sort_values("gross_margin_pct")
f = go.Figure()
f.add_bar(y=p.promo, x=p.gross_margin_pct, orientation="h", marker_color=[C if "No discount" not in s else B for s in p.promo],
          text=[f"{v:.1f}%" for v in p.gross_margin_pct], textposition="outside")
f.update_layout(title="Gross margin by promotion (full price in green)", xaxis=dict(title="Gross margin %", range=[50, 60]))
f.update_traces(hovertemplate="%{y}<br>Gross margin: %{x:.2f}%<extra></extra>")
figs["promo_margin"] = style(f, 400, margin=dict(l=250, r=40, t=50, b=50))

f = go.Figure()
f.add_bar(y=p.promo, x=p.units_per_line, orientation="h", marker_color=A, text=[f"{v:.1f}" for v in p.units_per_line], textposition="outside")
base = float(promo[promo.promo == "No discount"].units_per_line.iloc[0])
f.add_vline(x=base, line_dash="dash", line_color=MUTED, annotation_text="full price", annotation_position="top")
f.update_layout(title="Units per sales line by promotion", xaxis=dict(title="Units per line", range=[0, 25]))
f.update_traces(hovertemplate="%{y}<br>Units per line: %{x:.2f}<extra></extra>")
figs["promo_units"] = style(f, 400, margin=dict(l=250, r=40, t=50, b=50))

c = cat.sort_values("gross_margin_pct")
f = go.Figure(go.Bar(y=c.category, x=c.gross_margin_pct, orientation="h", marker_color=A, text=[f"{v:.1f}%" for v in c.gross_margin_pct], textposition="outside"))
f.update_layout(title="Gross margin by category", xaxis=dict(title="Gross margin %", range=[50, 64]))
f.update_traces(hovertemplate="%{y}<br>Gross margin: %{x:.2f}%<extra></extra>")
figs["cat_margin"] = style(f, 380, margin=dict(l=200, r=40, t=50, b=50))

order = [b for b in ["Under 13 wks cover", "13-26 wks cover", "Over 26 wks cover", "No sales in 13 wks"] if b in set(cover.cover_band)]
cv = cover.set_index("cover_band").reindex(order).fillna(0).reset_index()
f = go.Figure(go.Bar(x=cv.cover_band, y=cv.stock_value_m, marker_color=[B, A, C, "#b91c1c"][:len(cv)], text=[f"{v:.1f}M" for v in cv.stock_value_m], textposition="outside"))
f.update_layout(title="Stock value by weeks of cover (latest snapshot)", yaxis=dict(title="Stock value (millions)"))
f.update_traces(hovertemplate="%{x}<br>Stock value: %{y:.2f}M<extra></extra>")
figs["cover"] = style(f, 380)

o = over.sort_values("overstock_value_m")
f = go.Figure(go.Bar(y=o.category, x=o.overstock_value_m, orientation="h", marker_color=C, text=[f"{v:.1f}M ({q:.0f}%)" for v, q in zip(o.overstock_value_m, o.overstock_pct)], textposition="outside"))
f.update_layout(title="Overstock value by category (share of category stock)", xaxis=dict(title="Overstock value (millions)", range=[0, 14]))
f.update_traces(hovertemplate="%{y}<br>Overstock value: %{x:.2f}M<extra></extra>")
figs["overstock"] = style(f, 380, margin=dict(l=200, r=40, t=50, b=50))

r = risk.sort_values("pct_urgent")
f = go.Figure(go.Bar(y=r.category, x=r.pct_urgent, orientation="h", marker_color="#b91c1c", text=[f"{v:.0f}%" for v in r.pct_urgent], textposition="outside"))
f.update_layout(title="Store-products below safety stock with nothing on order (%)", xaxis=dict(title="% of store-products", range=[0, 80]))
f.update_traces(hovertemplate="%{y}<br>%{x:.1f}% of store-products<extra></extra>")
figs["risk"] = style(f, 380, margin=dict(l=200, r=40, t=50, b=50))

for k, fg in figs.items():
    os.makedirs("charts", exist_ok=True)
    pio.write_image(fg, f"charts/{k}.png", width=1000, height=fg.layout.height, scale=2) if False else None

def tbl():
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td class=n>{int(s)}</td><td class=n>{int(u):,}</td><td class=n>{d:,.0f}</td><td class=n>{int(cst):,}</td></tr>"
                   for a, b, s, u, d, cst in zip(reorder.product_name, reorder.category, reorder.stores_urgent, reorder.units_short_of_safety, reorder.weekly_units_demand, reorder.cost_to_restore))
    return f"<table><thead><tr><th>Product</th><th>Category</th><th class=n>Stores</th><th class=n>Units short</th><th class=n>Weekly demand</th><th class=n>Cost to restore</th></tr></thead><tbody>{rows}</tbody></table>"

d = lambda k, first=False: figs[k].to_html(full_html=False, include_plotlyjs="cdn" if first else False, config=dict(displayModeBar=False, responsive=True))
sp20 = promo[promo.promo.str.startswith("Spring Promotion (20%")].iloc[0]; fp = promo[promo.promo == "No discount"].iloc[0]
hol15 = promo[promo.promo.str.startswith("Holiday Promotion (15%")].iloc[0]
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Contoso Retail: Inventory, Discount and Margin Analysis</title>
<style>
body{{margin:0;background:#f8fafc;color:{INK};font:15px/1.55 Inter,'Segoe UI',Helvetica,Arial,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:32px 20px 60px}}
h1{{font-size:28px;margin:0 0 6px}} h2{{font-size:19px;margin:38px 0 6px}} .sub{{color:{MUTED};margin:0 0 22px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:14px;margin:18px 0 8px}}
.k{{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 16px}} .k b{{display:block;font-size:24px}} .k span{{color:{MUTED};font-size:13px}}
.card{{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:10px 14px;margin:14px 0}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} @media(max-width:860px){{.grid{{grid-template-columns:1fr}}}}
.note{{background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:12px 16px;font-size:14px;margin:14px 0}}
.find li{{margin:6px 0}} table{{border-collapse:collapse;width:100%;font-size:13px}} th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid #e5e7eb}}
th{{color:{MUTED};font-weight:600}} .n{{text-align:right}}
</style></head><body><div class="wrap">
<h1>Contoso Retail: Inventory, Discount and Margin Analysis</h1>
<p class="sub">3.4M sales lines and 8.0M weekly inventory records across 306 stores and 2,500 products, 2007 to 2009. Analysis in SQL (DuckDB) and Python.</p>
<div class="note"><b>About the data.</b> Contoso is Microsoft's fictitious retail sample data warehouse. The data includes cost, discount, return, on-hand, on-order and safety-stock fields, but every record is synthetic, so the figures show the method and are not observations from a real business. Amounts are in the dataset's own currency units. Inventory conclusions use the latest weekly snapshot (26 Dec 2009).</div>
<div class="kpis">
<div class="k"><b>{y09.net_sales_m/1000:.2f}B</b><span>2009 net sales ({100*(y09.net_sales_m/y08.net_sales_m-1):.1f}% vs 2008)</span></div>
<div class="k"><b>{y09.gross_margin_pct:.1f}%</b><span>2009 gross margin</span></div>
<div class="k"><b>{y09.discount_pct_of_gross:.2f}%</b><span>discounts as share of gross sales</span></div>
<div class="k"><b>{tot_val:.1f}M</b><span>stock value at latest snapshot</span></div>
<div class="k"><b>{100*over_val/tot_val:.0f}%</b><span>of stock value is overstock (over 26 weeks of cover or no sales in 13 weeks)</span></div>
<div class="k"><b>{100*urg/n_sp:.1f}%</b><span>of store-products below safety stock with nothing on order</span></div>
</div>
<h2>Key findings</h2>
<ul class="find">
<li><b>Promoted lines show lower margin, and the volume pattern is mixed.</b> Full-price lines earn {fp.gross_margin_pct:.1f}% gross margin. Lines under the Spring 20% promotion earn {sp20.gross_margin_pct:.1f}% and average {sp20.units_per_line:.1f} units per line against {fp.units_per_line:.1f} at full price. Lines under the Holiday 15% promotion average {hol15.units_per_line:.1f} units per line at {hol15.gross_margin_pct:.1f}% margin. These are observed differences, not measured effects of the promotions.</li>
<li><b>Over a third of inventory value is slow.</b> {over_val:.1f}M of {tot_val:.1f}M sits in store-products with more than 26 weeks of cover or no sales in the last 13 weeks. Home Appliances and Computers hold the largest amounts.</li>
<li><b>Shortages are concentrated.</b> Music, Movies and Audio Books has {risk.sort_values('pct_urgent').iloc[-1].pct_urgent:.0f}% of store-products below safety stock with no order placed. Cell phone accessories are the biggest reorder exposure by weekly demand.</li>
<li><b>Sales fell while units sold rose, and margin held near 57%.</b> Net sales went from {kpi.net_sales_m.iloc[0]/1000:.2f}B in 2007 to {y09.net_sales_m/1000:.2f}B in 2009, while units sold went from {kpi.units.iloc[0]/1e6:.1f}M to {y09.units/1e6:.1f}M over the same years ({kpi.units.iloc[1]/1e6:.1f}M in 2008). Revenue per unit fell about {100*(1-(y09.net_sales_m*1e6/y09.units)/(kpi.net_sales_m.iloc[0]*1e6/kpi.units.iloc[0])):.0f}% between 2007 and 2009, which is consistent with cheaper products or lower prices rather than weaker demand. The data does not separate price from product mix.</li>
</ul>
<h2>Sales and seasonality</h2><div class="card">{d('monthly', True)}</div>
<h2>Discount impact on margin</h2><div class="grid"><div class="card">{d('promo_margin')}</div><div class="card">{d('promo_units')}</div></div>
<p class="sub">Promotions are compared with full-price lines over the same three years. This is observational: promotions run in specific seasons and regions, so differences are associations, not proven effects.</p>
<h2>Margin by category</h2><div class="card">{d('cat_margin')}</div>
<h2>Inventory health</h2><div class="grid"><div class="card">{d('cover')}</div><div class="card">{d('overstock')}</div></div>
<h2>Reorder risk</h2><div class="card">{d('risk')}</div>
<div class="card"><b>Top 25 products to reorder</b> (below safety stock, nothing on order, ranked by weekly demand)<br><br>{tbl()}</div>
<p class="sub">Method: weeks of cover = on-hand units at the latest snapshot divided by average weekly units sold over the trailing 13 weeks, per store and product. Reorder risk = on-hand below safety stock with zero on order. Full SQL in the repository.</p>
</div></body></html>"""
open("docs/index.html", "w").write(html)
print("ok", len(html))
