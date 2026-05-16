"""
knowledge_base.py
All product/shop data for Christian Agyapong Sales.
To add a product: add a new dict to `business_data`.
"""

# The RAG system searches through this list to find answers.
# Each item has 'category', 'brand', 'content' (description/specs/price).
business_data = [
    # ── SHOP INFO ─────────────────────────────────────────
    {
        "category": "shop", "brand": "Christian Agyapong Sales",
        "in_stock": True, "stock_count": 1,
        "content": (
            "Christian Agyapong Sales is a multi-category retail platform with stores in Osu and Tema, Accra. "
            "We offer a wide range of products including Tech, Fashion, Food, Home, and Beauty items. "
            "Business Sales in Comfort is our mission."
        ),
    },
    {
        "category": "shop", "brand": "Contact & Delivery",
        "in_stock": True, "stock_count": 1,
        "content": (
            "WhatsApp: +233 5576 183 62. Delivery available within Accra/Tema for GHS 20-50 "
            "depending on distance. Same-day delivery for orders before 12 PM."
        ),
    },

    # ── TECH ──────────────────────────────────────────────
    {
        "category": "tech", "brand": "Samsung",
        "in_stock": True, "stock_count": 15,
        "content": (
            "Samsung Galaxy A05 (GHS 1,150), A15 (GHS 1,850), A35 (GHS 3,200), A55 (GHS 4,100). "
            "All come with 12 months warranty."
        ),
    },
    {
        "category": "tech", "brand": "Infinix",
        "in_stock": True, "stock_count": 12,
        "content": "Infinix Hot 40i (GHS 1,450), Note 40 Pro (GHS 3,850). Fast charging supported.",
    },
    {
        "category": "tech", "brand": "Tecno",
        "in_stock": True, "stock_count": 10,
        "content": "Tecno Spark 20 (GHS 1,200), Camon 30 (GHS 2,950). Excellent camera quality.",
    },
    {
        "category": "tech", "brand": "Laptops",
        "in_stock": True, "stock_count": 8,
        "content": (
            "Lenovo IdeaPad 3 (i3, 8GB RAM, 256GB SSD) - GHS 3,800. "
            "HP Laptop 15 (i5, 16GB RAM, 512GB SSD) - GHS 5,200."
        ),
    },
    {
        "category": "tech", "brand": "Television",
        "in_stock": True, "stock_count": 5,
        "content": "Samsung 43-inch Smart UHD TV (GHS 4,500). Hisense 55-inch 4K Smart TV (GHS 5,800).",
    },

    # ── FASHION ───────────────────────────────────────────
    {
        "category": "fashion", "brand": "Men's Wear",
        "in_stock": True, "stock_count": 50,
        "content": "Polo shirts (GHS 120), Formal shirts (GHS 150), Suits (GHS 850+). Variety of sizes.",
    },
    {
        "category": "fashion", "brand": "Women's Wear",
        "in_stock": True, "stock_count": 45,
        "content": "Dresses (GHS 180-450), Handbags (GHS 250+), Heels (GHS 300). Premium quality.",
    },
    {
        "category": "fashion", "brand": "Jeans and Trousers",
        "in_stock": False, "stock_count": 0,
        "content": "Jeans and chinos (GHS 180-650). Currently out of stock; restock coming soon.",
    },

    # ── FOOD ──────────────────────────────────────────────
    {
        "category": "food", "brand": "Staples and Groceries",
        "in_stock": True, "stock_count": 200,
        "content": (
            "Rice (5kg GHS 115-195), Gari, Beans, Palm Oil, Spices, Yam, Plantain, "
            "Tomatoes, Onions. Wholesale and retail available."
        ),
    },
    {
        "category": "food", "brand": "Snacks",
        "in_stock": True, "stock_count": 150,
        "content": (
            "Plantain chips, Chin chin, Biscuit packs, Chocolate, Soft drinks, Bottled water. "
            "Sold in packs and singles."
        ),
    },

    # ── HOME & BEAUTY ─────────────────────────────────────
    {
        "category": "home", "brand": "Appliances",
        "in_stock": True, "stock_count": 10,
        "content": "Microwaves (GHS 1,200), Blenders (GHS 450), Irons (GHS 250), Kettles (GHS 180).",
    },
    {
        "category": "beauty", "brand": "Skincare",
        "in_stock": True, "stock_count": 30,
        "content": "Body lotions, Face creams, Sunscreen, Serums. Brands: Nivea, Neutrogena, Cerave.",
    },
]
