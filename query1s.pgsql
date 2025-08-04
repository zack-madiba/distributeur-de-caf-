-- Active: 1751618385901@@127.0.0.1@5432@coffee_sales

-- Produit le plus vendu par saison seeon les quartiers (quantité vendus)
select store_location, season, sum(transaction_qty) 
from coffee_sales
where season ='spring'
group by store_location, season 
;

-- Produit le plus vendu par saison /  quartiers (recette)
select product_detail, store_location, season as season, sum(transaction_qty * unit_price) as recette
from coffee_sales
group by product_detail, store_location, season 
order by recette;

select  distinct  categorie from product_categorie;

select * from fact_sales limit 5;

SELECT p.product_detail as "Produit", 
sum(fs.quantity * fs.unit_price) as Recette
from fact_sales as fs
join product as p on fs.product_id = p.product_id
group by p.product_detail
order by Recette desc
limit 10
;