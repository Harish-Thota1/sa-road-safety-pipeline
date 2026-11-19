import json
import os
import urllib.request

PACKAGE_ID = "f8647df4-617b-439c-8de2-6aadfc84826a"  # SAPOL Expiation Notice System Data
API = f"https://data.sa.gov.au/data/api/3/action/package_show?id={PACKAGE_ID}"
OUT = "data/raw/expiation"

os.makedirs(OUT, exist_ok=True)

# Ask the Data.SA catalogue for every file in the dataset
with urllib.request.urlopen(API) as response:
    resources = json.load(response)["result"]["resources"]

for res in resources:
    name = res["name"]
    url = res["url"]

    # New layout (2022-23 onwards): camera offence reports only
    is_camera = name.startswith("Expiation Notices") and "Camera Offence" in name
    # Old layout (2011-12 to 2021-22): one combined file per year
    is_legacy = (
        name.startswith("Expiation Notices")
        and "Camera" not in name
        and "Manual" not in name
        and "Not Accept" not in name
    )
    if not (is_camera or is_legacy):
        continue

    filename = os.path.join(OUT, url.split("/")[-1])
    if os.path.exists(filename):
        print("Already have:", filename)
        continue

    print("Downloading:", name)
    urllib.request.urlretrieve(url, filename)

print("Done")

