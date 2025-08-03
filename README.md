# Analyse Complète des Ventes d'un Distributeur de Café



***

## I. Contexte du Projet

En tant que **Data Engineer** pour une enseigne spécialisée dans la vente de boissons chaudes à New York, j'ai développé une solution complète d'analyse des données de vente. L'entreprise exploite plusieurs magasins répartis sur différents quartiers et souhaite optimiser ses décisions commerciales grâce à l'analyse de ses données transactionnelles.

### Problématique Business

- Manque de visibilité sur les performances des différents points de vente
- Besoin d'identifier les tendances de consommation par période et localisation
- Optimisation de l'offre produit selon les préférences clients
- Amélioration de la planification des stocks et des ressources

***

## II. Objectifs

### Objectifs Techniques

- [x] Collecter et ingérer les données depuis un fichier Excel
- [x] Concevoir et implémenter une base de données PostgreSQL optimisée
- [x] Développer un pipeline ETL robuste pour le nettoyage des données
- [x] Créer un modèle en étoile (star schema) pour l'analyse
- [x] Enrichir les données avec la géolocalisation des magasins

### Objectifs Business

- [x] Analyser les performances de vente par magasin et période
- [x] Identifier les produits les plus populaires
- [x] Comprendre les patterns de consommation temporels
- [x] Fournir des insights exploitables aux équipes métier

***

## III. Architecture Technique

````
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Fichier       │    │   Pipeline       │    │   Base de       │
│   Excel         │───▶│   ETL            │───▶│   Données       │
│   Source        │    │   Python         │    │   PostgreSQL    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌─────────────────┐
                    │   Enrichissement │    │   Modélisation  │
                    │   Géolocalisation│    │   Star Schema   │
                    └──────────────────┘    └─────────────────┘
````

***

## IV. Pipeline de Données

### 1. Extraction des Données

- **Source** : Dataset Kaggle "Coffee Sales" (ahmedabbas757/coffee-sales)
- **Format** : Fichier Excel (.xlsx) téléchargé automatiquement
- **Volume** : Données transactionnelles de mars 2024
- **Contenu** : Transactions avec horodatage, produits, prix, quantités, types de paiement

### 2. Transformation et Nettoyage

```python
# Téléchargement automatique depuis Kaggle
def download_dataset(path):
    path = kagglehub.dataset_download("ahmedabbas757/coffee-sales")
    files = os.listdir(path)
    excel_files = [f for f in files if f.endswith('.xlsx')]
    df = pd.read_excel(f"{path}/{excel_files[0]}")
    shutil.rmtree(path)  # Nettoyage automatique
    return df

# Enrichissement temporel
dfcopy["hour"] = pd.to_datetime(dfcopy["transaction_time"], format="%H:%M:%S").dt.hour
dfcopy["day"] = dfcopy["transaction_date"].dt.day
dfcopy["month"] = dfcopy["transaction_date"].dt.strftime("%B")
dfcopy["weekday"] = dfcopy["transaction_date"].dt.strftime("%A")
dfcopy["time_slot"] = dfcopy["hour"].apply(get_tranche_horaire)
dfcopy["season"] = dfcopy["month"].map(seasons)

# Calcul du chiffre d'affaires
dfcopy["recipe"] = dfcopy["transaction_qty"] * dfcopy["unit_price"]
```

### 3. Enrichissement Géographique

- Utilisation de l'API Nominatim pour géolocaliser les magasins
- Ajout des coordonnées latitude/longitude
- Gestion des erreurs et timeout pour la robustesse

```python
geolocator = Nominatim(user_agent="geoapi")
for store in unique_stores:
    location = geolocator.geocode(store + ", New York, USA", timeout=10)
    # Traitement et sauvegarde des coordonnées
```

### 4. Chargement en Base

- Insertion en lots (chunks) de 1700 enregistrements
- Gestion des conflits avec `ON CONFLICT DO NOTHING`
- Optimisation avec indexation multi-colonnes

***

## V. Modélisation des Données

### Schéma en Étoile (Star Schema)

#### Table de Faits

**`fact_sales`** **fact_sales** **fact_sales** - Table centrale des transactions

- `id_transaction` (PK)
- `product_id` (FK)
- `location_id` (FK)
- `date_id` (FK)
- `season_id` (FK)
- `quantity`
- `unit_price`

#### Tables de Dimensions

**`product`** **product** **product** - Catalogue produit

- `product_id` (PK)
- `product_detail`
- `id_categorie` (FK)
- `id_type` (FK)
- `unit_price`

**`location_sales`** **location_sales** **location_sales** - Points de vente

- `id_location` (PK)
- `store_location`
- `latitude`
- `longitude`

**`date_sales`** **date_sales** **date_sales** - Dimension temporelle

- `id_date` (PK)
- `full_date`
- `day`, `weekday`, `month`, `year`
- `hour`, `time_slot`

**`product_categorie`** **product_categorie** **product_categorie** & **`product_type`** **product_type** **product_type** - Classifications produit

**`season`** **season** **season** - Saisons

### Optimisations Performantes

```sql
-- Index composites pour les requêtes analytiques
CREATE INDEX idx_fact_composite ON fact_sales(product_id, date_id);
CREATE INDEX idx_fact_sales_location ON fact_sales(location_id);
-- Analyse automatique des statistiques
ANALYZE fact_sales;
```

***

## VI. Traitement et Enrichissement

### Fonctionnalités Développées

#### 1. Téléchargement Automatisé depuis Kaggle

- **API Kaggle** pour récupération automatique des données
- **Détection automatique** des fichiers Excel dans le dataset
- **Nettoyage automatique** des fichiers temporaires après traitement

```python
def download_dataset(path):
    path = kagglehub.dataset_download("ahmedabbas757/coffee-sales")
    files = os.listdir(path)
    excel_files = [f for f in files if f.endswith('.xlsx')]
    if excel_files:
        df = pd.read_excel(f"{path}/{excel_files[0]}")
        shutil.rmtree(path)  # Nettoyage des fichiers temporaires
    return df
```

- **Tranches horaires** : matin, midi, après-midi, soir, nuit
- **Dimensions temporelles** : jour, semaine, mois, saison
- **Analyse des patterns** de consommation

#### 2. Segmentation Temporelle

- **Tranches horaires** : matin, midi, après-midi, soir, nuit
- **Dimensions temporelles** : jour, semaine, mois, saison
- **Analyse des patterns** de consommation

#### 3. Géolocalisation Automatique

- **API Nominatim** pour la géolocalisation des adresses
- **Coordonnées GPS** pour chaque point de vente
- **Gestion d'erreurs** robuste avec retry logic

#### 4. Calculs Métier

- **Chiffre d'affaires** par transaction
- **Métriques agrégées** par période et localisation
- **KPIs business** ready-to-use

***

## VII. Résultats et Insights

### Métriques Clés Calculées

- Chiffre d'affaires par magasin et période
- Top produits par catégorie et type
- Distribution des ventes par tranche horaire
- Performance saisonnière des points de vente
- Analyse géographique des performances

### Structure de Données Optimisée

- **149,116 transactions** traitées et nettoyées
- **Modèle normalisé** en 3NF avec star schema
- **Performance optimisée** avec indexation stratégique
- **Données géolocalisées** prêtes pour la cartographie

### Requêtes d'Exploitation Développées

#### 1. Top 5 Produits par Recette Globale

```sql
-- Analyse globale des meilleures performances produit
SELECT 
    p.product_detail AS "Produit", 
    pc.categorie AS Categorie,
    pt.type AS Type,
    TO_CHAR(SUM(fs.quantity * fs.unit_price), 'FM999999990.00 €') AS Recette,
    ls.store_location AS Ville
FROM fact_sales AS fs
JOIN product AS p ON fs.product_id = p.product_id
JOIN product_categorie AS pc ON pc.id_categorie = p.id_categorie  
JOIN product_type AS pt ON pt.id_type = p.id_type
JOIN location_sales AS ls ON ls.id_location = fs.location_id
JOIN date_sales AS ds ON ds.id_date = fs.date_id
GROUP BY p.product_detail, pc.categorie, pt.type, ls.store_location
ORDER BY SUM(fs.quantity * fs.unit_price) DESC
LIMIT 5;
```

![](5%20produits%20g%C3%A9n%C3%A9rant%20le%20plus%20de%20recette,%20avec%20leurs%20cat%C3%A9gories,%20types,%20et%20villes%20globalement.png)





#### 2. Meilleur Produit par Recette Mensuelle

```sql
-- Évolution du leadership produit avec fonctions de fenêtrage
WITH ventes_mensuelles AS (
    SELECT 
        p.product_detail AS produit,
        DATE_TRUNC('month', ds.full_date) AS mois,
        SUM(fs.quantity * fs.unit_price) AS recette
    FROM fact_sales fs
    JOIN product p ON fs.product_id = p.product_id
    JOIN date_sales ds ON fs.date_id = ds.id_date
    GROUP BY produit, mois
),
classement AS (
    SELECT *,
           RANK() OVER (PARTITION BY mois ORDER BY recette DESC) AS rang
    FROM ventes_mensuelles
)
SELECT mois, produit, recette
FROM classement
WHERE rang = 1
ORDER BY mois;
```

![](top%20de%20vente%20(recette)%20par%20mois.png)



#### 3. Produit le Plus Consommé par Mois (Quantité)

```sql
-- Analyse de volume avec ROW_NUMBER pour éliminer les ex-aequo
WITH ventes_mensuelles AS (
    SELECT 
        ds.id_date,
        p.product_detail as "Nom du produit",
        DATE_TRUNC('month', ds.full_date) AS mois,
        SUM(fs.quantity) AS quantite
    FROM fact_sales fs
    JOIN date_sales ds ON fs.date_id = ds.id_date
    JOIN product p ON fs.product_id = p.product_id
    GROUP BY mois, "Nom du produit", ds.id_date
),
classement AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY mois ORDER BY quantite DESC) AS rang
    FROM ventes_mensuelles
)
SELECT mois, "Nom du produit", quantite
FROM classement
WHERE rang = 1
ORDER BY mois;
```

![](images/le%20produit%20le%20plus%20consom%C3%A9%20(quantit%C3%A9)%20de%20chaque%20%20mois.png)



### Explications Techniques des Requêtes

**CTE (Common Table Expressions)** : Utilisation pour structurer les requêtes complexes et améliorer la lisibilité, notamment pour les calculs de dates dynamiques.

**Fonctions de Fenêtrage** :

- `RANK()` : Permet les ex-aequo avec des rangs identiques
- `ROW_NUMBER()` : Attribution de rangs uniques même en cas d'égalité

**Formatage des Données** :

- `TO_CHAR()` pour le formatage monétaire avec devise
- `DATE_TRUNC()` pour l'agrégation temporelle par mois

**Jointures Optimisées** : Star schema permettant des jointures efficaces entre la table de faits et les dimensions.

***

## Notes Techniques

### Stack Technique

- **Python 3.x** - Langage principal
- **PostgreSQL** - Base de données relationnelle
- **SQLAlchemy** - ORM et gestion des connexions
- **Pandas** - Manipulation et analyse des données
- **GeoPy** - Géolocalisation automatique
- **psycopg2** - Connecteur PostgreSQL
- **KaggleHub** - Téléchargement automatique des datasets

### Librairies Python

```python
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from geopy.geocoders import Nominatim
import kagglehub
import time
import locale
import os
import shutil
```

***

## IX. Guide d'Installation

### Prérequis

- Python 3.8+
- PostgreSQL 12+
- Compte Kaggle configuré avec API
- Packages Python requis (voir requirements.txt)

### Configuration Base de Données

```python
# Paramètres de connexion à ajuster
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres", 
    user="postgres",
    password="1212",
    port="5432"
)
```

***

## X. Utilisation

### Exécution du Pipeline Complet

```bash
python coffee_sales_etl.py
```

### Étapes d'Exécution

1. **Téléchargement** automatique depuis Kaggle via API
2. **Création** de la base de données `coffee_sales`
3. **Nettoyage** et enrichissement des données
4. **Géolocalisation** automatique des magasins
5. **Création** du modèle en étoile
6. **Indexation** et optimisation des performances

### Résultat Attendu

````
✅ Dataset téléchargé depuis Kaggle
✅ Base 'coffee_sales' créée
✅ Dataframe nettoyé: 149,116 lignes & 18 colonnes
✅ Tables dimensionnelles créées
✅ Données chargées et indexées
✅ Pipeline ETL terminé avec succès
````

***

## Notes Techniques

### Bonnes Pratiques Implémentées

- **Gestion des erreurs** robuste
- **Transactions atomiques** en base
- **Indexation optimisée** pour les performances
- **Code modulaire** et réutilisable
- **Documentation** inline du code

### Points d'Attention

- **Pause entre requêtes** API Nominatim (1 sec) pour respecter les conditions d'usage
- **Timeout** de géolocalisation configuré à 10s
- **Gestion mémoire** avec chunks de 1700 lignes
- **Validation des types** de données