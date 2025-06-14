CREATE DATABASE IF NOT EXISTS furniture_company
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE furniture_company;

CREATE TABLE materials_type (
  id_material_type               INT AUTO_INCREMENT PRIMARY KEY,
  material_type    VARCHAR(100) NOT NULL UNIQUE,
  loss_percentage  fLoat(5,2) NOT NULL
);

CREATE TABLE materials (
  id_material                 INT AUTO_INCREMENT PRIMARY KEY,
  name               VARCHAR(255) NOT NULL,
  id_material_type   INT NOT NULL,
  unit_price         float(10,2) NOT NULL,
  in_stock           float(12,2) NOT NULL,
  min_stock          float(12,2) NOT NULL,
  pack_size          float(12,2) NOT NULL,
  unit               VARCHAR(50) NOT NULL,
  FOREIGN KEY (id_material_type) REFERENCES materials_type(id_material_type)
);

CREATE TABLE products_type (
  id_product_type                    INT AUTO_INCREMENT PRIMARY KEY,
  product_type          VARCHAR(100) NOT NULL UNIQUE,
  type_coefficient      float(5,2) NOT NULL 
);

CREATE TABLE products (
  id_product                   INT AUTO_INCREMENT PRIMARY KEY,
  id_product_type      INT NOT NULL,
  name                 VARCHAR(255) NOT NULL,
  article                  VARCHAR(50)  NOT NULL UNIQUE,
  min_partner_price    float(10,2) NOT NULL,
  FOREIGN KEY (id_product_type) REFERENCES products_type(id_product_type)
);

CREATE TABLE material_products (
  id_materail_product                 INT AUTO_INCREMENT PRIMARY KEY,
  id_material        INT NOT NULL,
  id_product         INT NOT NULL,
  qty_per_unit       float(12,2) NOT NULL,
  FOREIGN KEY (id_material) REFERENCES materials(id_material),
  FOREIGN KEY (id_product) REFERENCES products(id_product)
);