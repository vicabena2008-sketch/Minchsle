"""
knowledge_base.py
All product/shop data for Min Chale.
To add a product: add a new dict to `business_data`.
"""

business_data = [
    # ── SHOP IDENTITY ─────────────────────────────────────
    {
        "category": "shop", "brand": "Min Chale",
        "in_stock": True, "stock_count": None,
        "content": (
            "Min Chale is a multi-category retail platform with stores in Osu and Tema, Accra. "
            "We sell Tech, Fashion, Food, Home Appliances, Beauty, and more with fast nationwide "
            "delivery across all 16 regions of Ghana."
        ),
    },

    # ── TECH ──────────────────────────────────────────────
    {
        "category": "tech", "brand": "Samsung",
        "in_stock": True, "stock_count": 18,
        "content": (
            "Official partner. Galaxy S24 Ultra (GHS 8,500), S23 (GHS 6,200), "
            "A35 (GHS 3,200), A15 (GHS 1,800), Galaxy Tabs from GHS 2,800."
        ),
    },
    {
        "category": "tech", "brand": "Apple",
        "in_stock": True, "stock_count": 7,
        "content": (
            "iPhone 16 from GHS 7,800, iPhone 15 from GHS 6,200, "
            "MacBook Air M2/M3 from GHS 9,500, MacBook Pro from GHS 14,500, AirPods from GHS 950."
        ),
    },
    {
        "category": "tech", "brand": "HP & Lenovo",
        "in_stock": True, "stock_count": 14,
        "content": (
            "HP Pavilion (GHS 4,200+), Victus Gaming (GHS 7,500+), EliteBook from GHS 5,800. "
            "Lenovo IdeaPad from GHS 3,800, ThinkPad series available."
        ),
    },
    {
        "category": "tech", "brand": "Infinix Tecno and Itel",
        "in_stock": True, "stock_count": 35,
        "content": (
            "Infinix Hot series (GHS 1,450-3,500), Tecno Spark and Camon (GHS 1,200-4,500), "
            "Itel phones from GHS 850. Very popular budget phones."
        ),
    },
    {
        "category": "tech", "brand": "Accessories",
        "in_stock": True, "stock_count": 60,
        "content": (
            "Power banks (GHS 120-650), Earphones and Headphones (GHS 80-850), "
            "Phone cases and screen protectors (GHS 50-350), Bluetooth speakers (GHS 150-1,200), "
            "Laptop bags (GHS 180-650)."
        ),
    },
    {
        "category": "tech", "brand": "Smart TV",
        "in_stock": False, "stock_count": 0,
        "content": (
            "Smart TVs (Samsung, LG) 32-inch to 65-inch. Prices from GHS 2,200 to GHS 8,500. "
            "Currently out of stock; restock expected soon."
        ),
    },

    # ── FASHION ───────────────────────────────────────────
    {
        "category": "fashion", "brand": "Shirts and Tops",
        "in_stock": True, "stock_count": 80,
        "content": (
            "Plain T-shirts (GHS 80-280), Polo shirts (GHS 150-380), "
            "Corporate and Oxford shirts (GHS 200-520). Custom printing and embroidery available."
        ),
    },
    {
        "category": "fashion", "brand": "Traditional Wear",
        "in_stock": True, "stock_count": 22,
        "content": (
            "Kente, Smock, Agbada, Senator, and Kaftan styles. "
            "Prices from GHS 450 to GHS 2,800. Ready-made and made-to-measure options."
        ),
    },
    {
        "category": "fashion", "brand": "Footwear and Bags",
        "in_stock": True, "stock_count": 45,
        "content": (
            "Sneakers (GHS 250-850), Corporate shoes (GHS 300-850), "
            "Ladies heels and flats (GHS 200-750), Quality handbags and backpacks (GHS 180-1,200)."
        ),
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
            "Chin Chin, Bofrot, Plantain Chips, Groundnut, Biscuits, Cakes from GHS 25 per pack. "
            "Wholesale packages for events and schools."
        ),
    },
    {
        "category": "food", "brand": "Packaged Meals",
        "in_stock": True, "stock_count": 30,
        "content": (
            "Jollof Rice, Waakye, Banku with Tilapia or Chicken, Fried Rice. "
            "Suitable for offices, events and home delivery in Accra."
        ),
    },

    # ── HOME & APPLIANCES ─────────────────────────────────
    {
        "category": "home", "brand": "Appliances",
        "in_stock": True, "stock_count": 25,
        "content": (
            "Standing Fans (GHS 350-950), Blenders (GHS 280-750), Rice Cookers (GHS 250-650), "
            "Electric Kettles (GHS 150-380), Irons (GHS 180-480), Refrigerators from GHS 2,800."
        ),
    },

    # ── BEAUTY ────────────────────────────────────────────
    {
        "category": "beauty", "brand": "Cosmetics and Hair",
        "in_stock": True, "stock_count": 55,
        "content": (
            "Skincare (Nivea, Ponds), Hair extensions, Wigs, Makeup kits, "
            "Perfumes, Soaps, Lotions. Popular brands available at good prices."
        ),
    },

    # ── PAYMENT, DELIVERY & POLICIES ──────────────────────
    {
        "category": "payment", "brand": "Payment Options",
        "in_stock": True, "stock_count": None,
        "content": (
            "MTN MoMo, Vodafone Cash, AirtelTigo Money, Bank Transfer, "
            "Cash on Delivery (Accra and Tema), Card payments in physical stores."
        ),
    },
    {
        "category": "delivery", "brand": "Nationwide Delivery",
        "in_stock": True, "stock_count": None,
        "content": (
            "Accra and Tema: Same day or Next day (GHS 30-80). "
            "Other regions: 1-4 business days (GHS 60-250 depending on weight and location). "
            "Tracking available."
        ),
    },
    {
        "category": "warranty", "brand": "Warranty Policy",
        "in_stock": True, "stock_count": None,
        "content": (
            "Tech and Home appliances come with minimum 3 months shop warranty plus "
            "manufacturer warranty where applicable. Fashion, Food and Beauty items are "
            "non-returnable except for defects."
        ),
    },
    {
        "category": "recommendation", "brand": "Special Offers",
        "in_stock": True, "stock_count": None,
        "content": (
            "We offer personalized recommendations based on budget and purpose. "
            "Students get special discounts on laptops, shirts, accessories and snacks. "
            "Bulk buyers enjoy wholesale pricing."
        ),
    },
]
