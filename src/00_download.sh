#!/usr/bin/env bash
# Downloads the Contoso Retail DW tables used here (about 220 MB zipped) into data/raw/.
set -euo pipefail
BASE=https://huggingface.co/datasets/jocapc/ContosoRetailDW/resolve/main
mkdir -p data/raw
for t in DimProduct DimProductCategory DimProductSubcategory DimPromotion DimStore DimChannel FactSales FactInventory; do
  curl -L -o data/raw/$t.zip "$BASE/$t.zip"
  mkdir -p data/raw/$t && unzip -o -q data/raw/$t.zip -d data/raw/$t
done
