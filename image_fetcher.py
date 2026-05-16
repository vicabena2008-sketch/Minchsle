"""
image_fetcher.py
Fetches product images via DuckDuckGo — no API key required.
Later: swap fetch_product_image() to pull from your Cloudinary store.
"""

import re
import json
import urllib.request
import urllib.parse


def is_image_accessible(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=3)
        return res.status == 200
    except Exception:
        return False


def fetch_product_image(product_name: str) -> str | None:
    """Return a working image URL for the given product name."""
    try:
        query = urllib.parse.quote(f"{product_name} product official")

        # Step 1 — get DuckDuckGo vqd session token
        ddg_url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images"
        req = urllib.request.Request(ddg_url, headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })
        html = urllib.request.urlopen(req, timeout=5).read().decode("utf-8", errors="ignore")

        vqd_match = re.search(r'vqd=["\'](\d[\d-]+)["\']', html)
        if not vqd_match:
            print(f"❌ Could not get vqd token for: {product_name}")
            return None
        vqd = vqd_match.group(1)

        # Step 2 — call the image JSON API
        api_url = (
            f"https://duckduckgo.com/i.js"
            f"?q={query}&o=json&p=1&s=0&u=bing&f=,,,,,&l=us-en&vqd={vqd}"
        )
        api_req = urllib.request.Request(api_url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer":    "https://duckduckgo.com/",
        })
        raw = urllib.request.urlopen(api_req, timeout=5).read().decode("utf-8", errors="ignore")
        data = json.loads(raw)

        results = data.get("results", [])
        if not results:
            print(f"❌ No images found for: {product_name}")
            return None

        for item in results[:5]:
            url = item.get("image", "")
            if url and is_image_accessible(url):
                return url

    except Exception as e:
        print(f"❌ Image fetch error for '{product_name}': {e}")

    return None


def extract_product_name(context_docs: list) -> str:
    """Pull the brand name from the first retrieved doc string."""
    if not context_docs:
        return ""
    for line in context_docs[0].split("\n"):
        if line.startswith("BRAND"):
            return line.split(":", 1)[-1].strip()
    return ""
