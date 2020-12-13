CREATE TABLE Category (
    id SMALLINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    PRIMARY KEY (id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE Product (
    id SMALLINT UNSIGNED AUTO_INCREMENT,
    code BIGINT UNSIGNED UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    generic_name TINYTEXT,
    stores TINYTEXT,
    countries TEXT,
    PRIMARY KEY (id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE Product_category (
    product_id SMALLINT UNSIGNED,
    category_id SMALLINT UNSIGNED,
    CONSTRAINT for_key_1 FOREIGN KEY (product_id) REFERENCES Product(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT for_key_2 FOREIGN KEY (category_id) REFERENCES Category(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE uni_prod_cat (product_id, category_id)
)
ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE Substitute (
    prod_id_orig SMALLINT UNSIGNED,
    prod_id_subs SMALLINT UNSIGNED,
    CONSTRAINT for_key_3 FOREIGN KEY (prod_id_orig) REFERENCES Product(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT for_key_4 FOREIGN KEY (prod_id_subs) REFERENCES Product(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE INDEX unique_substitute(prod_id_orig, prod_id_subs)
)
ENGINE=InnoDB CHARSET=utf8;
