import requests
from bs4 import BeautifulSoup
import pandas as pd

# ETF holdings URLs (can add more)
ETF_URLS = {
    "XYLD": "https://www.globalxetfs.com/funds/xyld/",
    "QYLD": "https://www.globalxetfs.com/funds/qyld/",
    "JEPI": "https://am.jpmorgan.com/us/en/asset-management/adv/products/jepi/",
    "RYLD": "https://www.globalxetfs.com/funds/ryld/"
}

def fetch_etf_holdings(url, etf_name):
    """Fetch holdings table from ETF provider page."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {etf_name}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"No table found for {etf_name}")
        return None

    df = pd.read_html(str(table))[0]
    df.columns = [col.strip() for col in df.columns]
    df['ETF'] = etf_name  # add ETF name column
    return df

def main():
    all_holdings = []

    for etf_name, url in ETF_URLS.items():
        print(f"Fetching holdings for {etf_name}...")
        df = fetch_etf_holdings(url, etf_name)
        if df is not None:
            all_holdings.append(df)

    if all_holdings:
        combined_df = pd.concat(all_holdings, ignore_index=True)
        # Save CSV
        combined_df.to_csv("all_etf_holdings.csv", index=False)
        print("Saved all ETF holdings to all_etf_holdings.csv")
        # Save HTML
        combined_df.to_html("all_etf_holdings.html", index=False)
        print("Saved all ETF holdings to all_etf_holdings.html")
    else:
        print("No holdings data fetched.")

if __name__ == "__main__":
    main()
