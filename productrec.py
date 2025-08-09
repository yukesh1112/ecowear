import pandas as pd

def get_info(url, img):
    # Ensure image URL starts with https://
    if not img.startswith("http"):
        img = "https://" + img.lstrip("/")

    # Extract store name safely
    store_name = url.replace("https://", "").replace("http://", "")
    if ".com" in store_name:
        store_name = store_name[0:store_name.index(".com")]
    store_name = store_name.replace("www.", "").replace("-", " ").upper()

    # Extract product name safely
    if "products/" in url:
        product_name = url.split("products/", 1)[1].replace("-", " ")
    else:
        # fallback: take last part of the URL
        product_name = url.rstrip("/").split("/")[-1].replace("-", " ")

    return (store_name, product_name, url, img)

def give_rec(type, num):
    sel = 0
    rec_list = []
    df = pd.read_csv(type+"_22.csv")
    del df['Unnamed: 0']

    prev = df["links"][0]
    prev_index = prev[0:prev.index(".")]

    for i in range(0, len(df), 1):
        line = df["links"][i]
        index = df["links"][i][0:line.index(".")]

        if i == 0:
            rec_list.append(get_info(df.iloc[i][0], df.iloc[i][1]))
            sel += 1
        elif index != prev_index and sel < num:
            rec_list.append(get_info(df.iloc[i][0], df.iloc[i][1]))
            sel += 1

        if sel == num:
            break

        prev = line
        prev_index = index

    return rec_list
