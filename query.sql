SELECT
  store_location,
  latitude,
  longitude,
  sum(transaction_qty) AS total_vendu,
  sum(recipe) AS total_revenu
FROM
  coffee_sales
GROUP BY
  store_location,
  latitude,
  longitude
ORDER BY
  total_vendu DESC;