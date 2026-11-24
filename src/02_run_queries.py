"""Run every SQL file in order against data/contoso.duckdb; write results/*.csv."""
import duckdb, glob, os
con = duckdb.connect("data/contoso.duckdb")
os.makedirs("results", exist_ok=True)
for f in sorted(glob.glob("sql/*.sql")):
    name = os.path.basename(f)[:-4]
    text = "\n".join(l for l in open(f).read().splitlines() if not l.strip().startswith("--"))
    stmts = [s.strip() for s in text.split(";") if s.strip()]
    res = None
    for s in stmts:
        r = con.execute(s)
        if s.upper().startswith(("SELECT", "WITH")):
            res = r.fetchdf()
    if res is not None:
        res.to_csv(f"results/{name}.csv", index=False)
        print("==", name); print(res.head(12).to_string(index=False)); print()
