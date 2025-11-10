# Real-Time Product Recommendations System

## Overview
EcoWear now uses a real-time product recommendation system that fetches actual sustainable fashion products from curated eco-friendly brands.

## How It Works

### 1. Primary Source: Real-Time Curated Data
The system first attempts to fetch products from `realtime_products.py`, which contains:
- **Curated sustainable brands**: Patagonia, Everlane, Reformation, Allbirds, Veja, Pact, etc.
- **Real product links**: Direct links to actual products on brand websites
- **Product images**: Real product images from sustainable fashion brands
- **Category mapping**: Products organized by clothing category (t-shirt, dress, pants, etc.)

### 2. Fallback: CSV Data
If real-time fetching fails, the system falls back to CSV files with backup product data.

## Supported Sustainable Brands

### Clothing
- **Patagonia**: Outdoor clothing with strong environmental commitment
- **Everlane**: Transparent pricing and ethical manufacturing
- **Reformation**: Carbon-neutral fashion brand
- **Pact**: Organic cotton basics
- **Tentree**: Plants 10 trees for every purchase
- **Organic Basics**: Sustainable essentials
- **Nudie Jeans**: Organic denim with free repairs

### Footwear
- **Allbirds**: Sustainable wool and tree fiber shoes
- **Veja**: Fair trade sneakers made with organic materials

## Product Categories
- T-shirts
- Shirts
- Pants
- Dresses
- Shoes
- Shorts
- Longsleeve
- Outwear
- Skirts
- Hats

## Data Structure
Each product recommendation includes:
1. **Store**: Brand name
2. **Name**: Product name
3. **Link**: Direct URL to product page
4. **Image_URL**: Product image URL

## Extending the System

### Adding New Brands
Edit `realtime_products.py` and add to the `sustainable_products` dictionary:

```python
'category': [
    {
        'Store': 'Brand Name',
        'Name': 'Product Name',
        'Link': 'https://brand.com/product',
        'Image_URL': 'https://brand.com/image.jpg'
    },
]
```

### Adding API Integration
To integrate with real e-commerce APIs:
1. Get API keys from sustainable fashion platforms
2. Update `get_real_products_api()` function
3. Add API request logic with proper error handling

## Future Enhancements
- Integration with Good On You API for brand ratings
- Real-time web scraping for latest products
- Price comparison across sustainable brands
- User preference learning
- Seasonal product recommendations

## Testing
Run the test script:
```bash
python realtime_products.py
```

This will fetch sample products and display them in the console.
