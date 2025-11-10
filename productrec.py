import pandas as pd
from realtime_products import get_real_products_api

def give_rec(category, num_recommendations=2):
    """
    Fetches real-time product recommendations from sustainable fashion brands.
    Falls back to CSV data if real-time fetching fails.
    """
    
    # Try to get real-time products first
    try:
        real_products = get_real_products_api(category, num_recommendations)
        if real_products and len(real_products) >= num_recommendations:
            return real_products
    except Exception as e:
        print(f"Real-time fetch failed, using fallback: {e}")
    
    # Fallback to CSV data if real-time fails
    return give_rec_from_csv(category, num_recommendations)


def give_rec_from_csv(category, num_recommendations=2):
    """
    Finds the correct CSV file for a given category, reads it,
    and returns a specified number of random product recommendations.
    """
    
    # This dictionary maps the 10 class names to their corresponding CSV data files.
    # This makes the function flexible and easy to update.
    category_to_filename = {
        'dress': 'dresses_22.csv',
        'hat': 'hats.csv',
        'longsleeve': 'longsleeves.csv',
        'outwear': 'outwear.csv',
        'pants': 'pants.csv',
        'shirt': 'shirts.csv',
        'shoes': 'shoes.csv',
        'shorts': 'shorts.csv',
        'skirt': 'skirts.csv',
        't-shirt': 't-shirts.csv',
        # Mappings for old categories can be kept for backward compatibility if needed
        'tops': 'tops_22.csv',
        'bottoms': 'bottoms_22.csv'
    }

    filename = category_to_filename.get(category.lower())

    if not filename:
        print(f"Warning: No data file found for category '{category}'")
        return []

    try:
        # Read the product data from the correct CSV file
        df = pd.read_csv(filename)

        # Robustly check for and remove the old index column if it exists
        if 'Unnamed: 0' in df.columns:
            del df['Unnamed: 0']

        # Ensure we don't ask for more recommendations than available products
        if len(df) < num_recommendations:
            num_recommendations = len(df)
            
        if num_recommendations == 0:
            return []

        # Get a random sample of products from the dataframe, which is a simple and effective
        # way to provide varied recommendations.
        recommendations_df = df.sample(n=num_recommendations)
        
        # Convert the DataFrame rows to a list of lists, which server.py can use.
        # This uses the correct, case-sensitive column names from the new CSV files.
        rec_list = []
        for index, row in recommendations_df.iterrows():
            rec_list.append([
                row['Store'],
                row['Name'],
                row['Link'],
                row['Image_URL']
            ])
            
        return rec_list

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found for category '{category}'.")
        return []
    except Exception as e:
        print(f"An error occurred in give_rec for category '{category}': {e}")
        return []