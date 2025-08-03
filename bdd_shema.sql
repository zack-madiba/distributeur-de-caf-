CREATE TABLE "date_sales" (
  "id_date" INT PRIMARY KEY,
  "full_date" date UNIQUE,
  "day" int,
  "weekday" varchar(50),
  "month" datetime,
  "year" int,
  "hour" int,
  "time_slot" varchar(25)
);

CREATE TABLE "season" (
  "id_season" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "fact_sales" (
  "id_transaction" serial PRIMARY KEY,
  "product_id" int,
  "location_id" int,
  "date_id" int,
  "season_id" int,
  "quantity" int,
  "unit_price" int
);

CREATE TABLE "product" (
  "id_product" INT PRIMARY KEY,
  "name" varchar,
  "category_id" int,
  "type_id" int
);

CREATE TABLE "product_categorie" (
  "id_categorie" Serial PRIMARY KEY,
  "categorie" varchar(50)
);

CREATE TABLE "product_type" (
  "id_type" serial PRIMARY KEY,
  "type" varchar(50)
);

CREATE TABLE "location_sales" (
  "id_location" INT PRIMARY KEY,
  "store" varchar,
  "latitude" float,
  "longitude" float
);

ALTER TABLE "fact_sales" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("id_product");

ALTER TABLE "fact_sales" ADD FOREIGN KEY ("location_id") REFERENCES "location_sales" ("id_location");

ALTER TABLE "fact_sales" ADD FOREIGN KEY ("date_id") REFERENCES "date_sales" ("id_date");

ALTER TABLE "fact_sales" ADD FOREIGN KEY ("season_id") REFERENCES "season" ("id_season");

ALTER TABLE "product" ADD FOREIGN KEY ("category_id") REFERENCES "product_categorie" ("id_categorie");

ALTER TABLE "product" ADD FOREIGN KEY ("type_id") REFERENCES "product_type" ("id_type");
