import pandas as pd

# File paths
db_file = 'db.csv'
store_file = 'tops.csv'

# Read CSVs
db_df = pd.read_csv(db_file)
store_df = pd.read_csv(store_file)
base = 'https://directory.goodonyou.eco'

def query(store_name):
    link_rec = []
    generic_name = store_name.lower().replace(' ', '-')
    
    # Case-insensitive search to avoid errors
    store_info = db_df[db_df['store name'].str.contains(generic_name, case=False, na=False)]
    
    # Check if store is found
    if store_info.empty:
        print(f"Error: Store '{store_name}' not found.")
        return [0, []]
    
    # Get store rating and recommendations
    rate_num = store_info['rating'].item()
    name_rec = [store_info['r1'].item(), store_info['r2'].item(), store_info['r3'].item()]
    
    # If rating < 4, get recommended store links
    if rate_num < 4:
        for name in name_rec:
            tops_name = store_df[store_df['store name'].str.contains(name, case=False, na=False)]
            if not tops_name.empty:
                tops_link = tops_name['brand link'].iloc[0]
                link_rec.append(base + tops_link)
    
    return [rate_num, link_rec]

# Example Usage
# print(query('girlfriend colLectIVe'))
