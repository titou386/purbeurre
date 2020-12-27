DROP TABLE IF EXISTS substitute;
DROP TABLE IF EXISTS product_category;
DROP TABLE IF EXISTS nutriments;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id SMALLINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(75) UNIQUE NOT NULL,
    PRIMARY KEY (id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE product (
    id SMALLINT UNSIGNED AUTO_INCREMENT,
    code BIGINT UNSIGNED UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    generic_name TINYTEXT,
    stores TINYTEXT,
    countries TEXT,
    PRIMARY KEY (id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE nutriment (
    product_id SMALLINT UNSIGNED UNIQUE,
    nova_group CHAR(1),
    nutriscore_grade CHAR(1),
    fat_100g FLOAT,
    saturated_fat_100g FLOAT,
    salt_100g FLOAT,
    sugars_100g FLOAT,
    CONSTRAINT prod_nutri FOREIGN KEY (product_id) REFERENCES product(id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE product_category (
    product_id SMALLINT UNSIGNED,
    category_id SMALLINT UNSIGNED,
    CONSTRAINT for_key_1 FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT for_key_2 FOREIGN KEY (category_id) REFERENCES category(id),
    UNIQUE uni_prod_cat (product_id, category_id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE substitute (
    product_id SMALLINT UNSIGNED UNIQUE,
    subs_product_id SMALLINT UNSIGNED,
    CONSTRAINT for_key_4 FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT for_key_5 FOREIGN KEY (subs_product_id) REFERENCES product(id),
    UNIQUE INDEX unique_substitute(product_id, subs_product_id)
)
ENGINE=InnoDB CHARSET=utf8;
