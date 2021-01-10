DROP TABLE IF EXISTS substitution;
DROP TABLE IF EXISTS product_category;
DROP TABLE IF EXISTS nutriments;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id SMALLINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(130) UNIQUE NOT NULL,
    PRIMARY KEY (id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE product (
    id SMALLINT UNSIGNED AUTO_INCREMENT,
    code BIGINT UNSIGNED UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    generic_name TEXT,
    quantity VARCHAR(100),
    stores TINYTEXT,
    countries TEXT,
    PRIMARY KEY (id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE nutriments (
    product_id SMALLINT UNSIGNED NOT NULL UNIQUE,
    nova_group CHAR(1),
    nutriscore_grade CHAR(1),
    energy_kcal_100g DECIMAL(6,2),
    fat_100g DECIMAL(5,2),
    saturated_fat_100g DECIMAL(5,2),
    carbohydrates_100g DECIMAL(5,2),
    sugars_100g DECIMAL(5,2),
    fiber_100g DECIMAL(5,2),
    proteins_100g DECIMAL(5,2),
    salt_100g DECIMAL(5,2),
    energy_kcal_unit VARCHAR(10),
    fat_unit VARCHAR(10),
    saturated_fat_unit VARCHAR(10),
    carbohydrates_unit VARCHAR(10),
    sugars_unit VARCHAR(10),
    fiber_unit VARCHAR(10),
    proteins_unit VARCHAR(10),
    salt_unit VARCHAR(10),
    CONSTRAINT prod_nutri FOREIGN KEY (product_id) REFERENCES product(id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE product_category (
    product_id SMALLINT UNSIGNED NOT NULL,
    category_id SMALLINT UNSIGNED,
    CONSTRAINT key_1 FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT key_2 FOREIGN KEY (category_id) REFERENCES category(id),
    UNIQUE uni_prod_cat (product_id, category_id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE substitution (
    product_id SMALLINT UNSIGNED NOT NULL UNIQUE,
    subs_product_id SMALLINT UNSIGNED,
    CONSTRAINT key_3 FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT key_4 FOREIGN KEY (subs_product_id) REFERENCES product(id)
)
ENGINE=InnoDB CHARSET=utf8;
