-- Active: 1751618385901@@127.0.0.1@5432@coffee_sales
-- Active: 1751618385901@@127.0.0.1@5432@coffee_sales

-- 5 produits générant le plus de recette, avec leurs catégories, types, et villes globalement
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

-- 5 produits générant le plus de recette, avec leurs catégories, types, et villes es deux derniers mois

WITH limites_dates AS (
    SELECT 
        MAX(full_date) AS max_date,
        DATE_TRUNC('month', MAX(full_date)) - INTERVAL '1 month' AS debut_avant_dernier_mois
    FROM date_sales
)

SELECT 
    p.product_detail AS "Produit", 
    pc.categorie AS Categorie,
    pt.type AS Type,
    SUM(fs.quantity * fs.unit_price) AS Recette,
    ls.store_location AS Ville
FROM fact_sales fs
JOIN product p ON fs.product_id = p.product_id
JOIN product_categorie pc ON pc.id_categorie = p.id_categorie
JOIN product_type pt ON pt.id_type = p.id_type
JOIN location_sales ls ON ls.id_location = fs.location_id
JOIN date_sales ds ON ds.id_date = fs.date_id
JOIN limites_dates ld ON TRUE
WHERE ds.full_date >= ld.debut_avant_dernier_mois
  AND ds.full_date <= ld.max_date
GROUP BY p.product_detail, pc.categorie, pt.type, ls.store_location
ORDER BY Recette DESC
LIMIT 5;



-- top de vente (recette) par mois


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



-- le produit le plus consomé (quantité) de chaque  mois

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
