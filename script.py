
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import time
from geopy.geocoders import Nominatim
import locale
import os
import shutil



print("Debut de l'execution du script de téléchargement des données...")

# Téléchargement et affichage du jeu de données "Coffee Sales" depuis Kaggle
# Assurez-vous d'avoir installé kagglehub avec `pip install kagglehub`
def download_dataset(path):
    df = None
    try:
        path = kagglehub.dataset_download("ahmedabbas757/coffee-sales")
        
        files = os.listdir(path)
        excel_files = [f for f in files if f.endswith('.xlsx')]
        
        if excel_files:
            df = pd.read_excel(f"{path}/{excel_files[0]}")
            shutil.rmtree(path)
        else:
            print("Aucun fichier CSV trouvé dans le dossier téléchargé.")
        
    except Exception as e:
        print(f"Erreur : {e}")

    return df

download_dataset("coffee_sales")


df = download_dataset("coffee_sales")

print("Fin de l'execution du script de téléchargement des données")
print("\n=====================================================================================================================================")
print("Debut de la creation de la base de donné coffee_sales")

# Création de la base si elle n'existe pas
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="1212", port="5432")
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname = 'coffee_sales'")
if not cur.fetchone():
    cur.execute("CREATE DATABASE coffee_sales ENCODING 'UTF8';")
    print("Base 'coffee_sales' créée.")
else:
    print("La base 'coffee_sales' existe déjà.")
cur.close()
conn.close()

# Connexion avec SQLAlchemy
engine = create_engine('postgresql+psycopg2://postgres:1212@localhost:5432/coffee_sales')
df.to_sql('coffee_sales', engine, if_exists='replace', chunksize=1700, index=False)
print("Table 'coffee_sales' créée avec succès.")

print("\nFin de l'execution du script de creation de la base de donnée coffee_sales")
print("\n=====================================================================================================================================")
print("Début du nettoyage des données et enrichissement du dataframe")

# Nettoyage
locale.setlocale(locale.LC_TIME, 'en_EN.UTF-8')
dfcopy = df.copy()
dfcopy["recipe"] = dfcopy["transaction_qty"] * dfcopy["unit_price"]
dfcopy["transaction_date"] = pd.to_datetime(dfcopy["transaction_date"])
dfcopy["hour"] = pd.to_datetime(dfcopy["transaction_time"], format="%H:%M:%S").dt.hour
dfcopy["day"] = dfcopy["transaction_date"].dt.day
dfcopy["month"] = dfcopy["transaction_date"].dt.strftime("%B")
dfcopy["weekday"] = dfcopy["transaction_date"].dt.strftime("%A")
dfcopy["year"] = dfcopy["transaction_date"].dt.year
dfcopy['full_date'] = dfcopy['transaction_date'].dt.strftime('%Y-%m-%d')

def get_tranche_horaire(hour):
    if 5 <= hour < 12:
        return "matin"
    elif 12 <= hour < 14:
        return "midi"
    elif 14 <= hour < 18:
        return "après-midi"
    elif 18 <= hour < 22:
        return "soir"
    else:
        return "nuit"

dfcopy["time_slot"] = dfcopy["hour"].apply(get_tranche_horaire)

seasons = {"March": "spring", "April": "spring", "May": "spring",
           "June": "summer", "July": "summer", "August": "summer",
           "September": "autumn", "October": "autumn", "November": "autumn",
           "December": "winter", "January": "winter", "February": "winter"}
dfcopy["season"] = dfcopy["month"].map(seasons)

geolocator = Nominatim(user_agent="geoapi")
unique_stores = dfcopy['store_location'].dropna().unique()
locations = []

for store in unique_stores:
    try:
        location = geolocator.geocode(store + ", New York, USA", timeout=10)
        if location:
            locations.append({"store_name": store, "latitude": location.latitude, "longitude": location.longitude})
        else:
            locations.append({"store_name": store, "latitude": None, "longitude": None})
        time.sleep(1)
    except Exception as e:
        print(f"Erreur avec {store}: {e}")

geo_df = pd.DataFrame(locations)
coord_dict = geo_df.set_index("store_name").to_dict("index")
dfcopy[["latitude", "longitude"]] = pd.DataFrame(dfcopy["store_location"].map(lambda x: coord_dict.get(x, {"latitude": None, "longitude": None})).tolist(), index=dfcopy.index)
dfcopy['latitude'] = pd.to_numeric(dfcopy['latitude'], errors='coerce')
dfcopy['longitude'] = pd.to_numeric(dfcopy['longitude'], errors='coerce')
dfcopy['recipe'] = pd.to_numeric(dfcopy['recipe'], errors='coerce')
dfcopy = dfcopy.dropna(subset=['latitude', 'longitude'])
dfcopy.to_sql('coffee_sales', engine, if_exists='replace', chunksize=1700, index=False)

print(f"Dataframe nettoyé {dfcopy.shape[0]} lignes & {dfcopy.shape[1]} colonnes")

print("Fin du nettoyage et insertion des données nettoyées en base")
print("\n=====================================================================================================================================")
print("Debut de creation des tables dimensionnelles et insertion")

# Création des tables
schemas = [
    """CREATE TABLE IF NOT EXISTS product_categorie (id_categorie SERIAL PRIMARY KEY, categorie VARCHAR(50) UNIQUE);""",
    """CREATE TABLE IF NOT EXISTS product_type (id_type SERIAL PRIMARY KEY, type VARCHAR(50) UNIQUE);""",
    """CREATE TABLE IF NOT EXISTS location_sales (id_location SERIAL PRIMARY KEY, store_location VARCHAR(100) UNIQUE, latitude FLOAT, longitude FLOAT);""",
    """CREATE TABLE IF NOT EXISTS date_sales (id_date SERIAL PRIMARY KEY, full_date DATE UNIQUE, day INT, weekday VARCHAR(50), month VARCHAR(50), year INT, hour INT, time_slot VARCHAR(25));""",
    """CREATE TABLE IF NOT EXISTS season (id_season SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE);""",
    """CREATE TABLE IF NOT EXISTS product (product_id SERIAL PRIMARY KEY, product_detail VARCHAR(255) UNIQUE, id_categorie INT REFERENCES product_categorie(id_categorie), id_type INT REFERENCES product_type(id_type), unit_price DECIMAL(10,2));""",
    """CREATE TABLE IF NOT EXISTS fact_sales (id_transaction INT PRIMARY KEY, product_id INT REFERENCES product(product_id), location_id INT REFERENCES location_sales(id_location), date_id INT REFERENCES date_sales(id_date), season_id INT REFERENCES season(id_season), quantity INT, unit_price DECIMAL(10,2));"""
]

inserts = [
    """INSERT INTO product_categorie (categorie) SELECT DISTINCT product_category FROM coffee_sales ON CONFLICT (categorie) DO NOTHING;""",
    """INSERT INTO product_type (type) SELECT DISTINCT product_type FROM coffee_sales ON CONFLICT (type) DO NOTHING;""",
    """INSERT INTO location_sales (store_location, latitude, longitude) SELECT DISTINCT store_location, latitude, longitude FROM coffee_sales ON CONFLICT (store_location) DO NOTHING;""",
    """INSERT INTO date_sales (full_date, day, weekday, month, year, hour, time_slot) SELECT DISTINCT transaction_date::DATE, day, weekday, month, year, hour, time_slot FROM coffee_sales ON CONFLICT (full_date) DO NOTHING;""",
    """INSERT INTO season (name) SELECT DISTINCT season FROM coffee_sales ON CONFLICT (name) DO NOTHING;""",
    """INSERT INTO product (product_detail, id_categorie, id_type, unit_price) SELECT DISTINCT cs.product_detail, pc.id_categorie, pt.id_type, cs.unit_price FROM coffee_sales cs JOIN product_categorie pc ON cs.product_category = pc.categorie JOIN product_type pt ON cs.product_type = pt.type ON CONFLICT (product_detail) DO NOTHING;""",
    """INSERT INTO fact_sales (id_transaction, product_id, location_id, date_id, season_id, quantity, unit_price) SELECT cs.transaction_id, p.product_id, ls.id_location, ds.id_date, s.id_season, cs.transaction_qty, cs.unit_price FROM coffee_sales cs JOIN product p ON cs.product_detail = p.product_detail JOIN location_sales ls ON CAST(cs.store_location AS VARCHAR) = ls.store_location JOIN date_sales ds ON cs.transaction_date::DATE = ds.full_date JOIN season s ON cs.season = s.name;"""
]

with engine.connect() as conn:
    trans = conn.begin()
    try:
        for schema in schemas:
            conn.execute(text(schema))
        for insert in inserts:
            conn.execute(text(insert))

        # Indexation
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_id);
            CREATE INDEX IF NOT EXISTS idx_fact_sales_location ON fact_sales(location_id);
            CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(date_id);
            CREATE INDEX IF NOT EXISTS idx_fact_sales_season ON fact_sales(season_id);
            CREATE INDEX IF NOT EXISTS idx_fact_composite ON fact_sales(product_id, date_id);
            ANALYZE fact_sales;
        """))

        trans.commit()
        print("Operation completed successfully: tables created, data loaded, and indexes optimized")
    except Exception as e:
        trans.rollback()
        print("Error occurred:", e)

print("\n=================================================== FIN D'EXECUTION DU SCRIPT COMPLET ===============================")
