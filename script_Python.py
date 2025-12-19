import requests
import csv

def fetch_champagne_products():
    # URL de l'API OpenFoodFacts pour rechercher des produits à base de "champagne"
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": "",
        "ingredients_tags": "champagne",
        "page_size": 10,
        "json": 1
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("products", [])
    else:
        print(f"Erreur lors de la requête API: {response.status_code}")
        return []

def save_to_csv(products, filename):
    # Colonnes à inclure dans le fichier CSV
    fields = ["foodId", "label", "category", "foodContentsLabel", "image"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for product in products:
            writer.writerow({
                "foodId": product.get("id", "N/A"),
                "label": product.get("product_name", "N/A"),
                "category": ", ".join(product.get("categories_tags", [])),
                "foodContentsLabel": product.get("ingredients_text", "N/A"),
                "image": product.get("image_url", "N/A")
            })

if __name__ == "__main__":
    # Récupération des produits
    products = fetch_champagne_products()

    if products:
        # Sauvegarde dans un fichier CSV
        save_to_csv(products, "champagne_products.csv")
        print("Fichier 'champagne_products.csv' créé avec succès.")
    else:
        print("Aucun produit trouvé.")
