-- CREATE USER 'stockcats'@'localhost' IDENTIFIED BY 'stockcats';
-- GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP ON *.* TO 'stockcats'@'localhost';

-- -----------------------------------------------------------------------------

DROP TABLE IF EXISTS FinancialStatementEntry;
DROP TABLE IF EXISTS FinancialStatement;
DROP TABLE IF EXISTS DateFrame;
DROP TABLE IF EXISTS StockCode;

-- -----------------------------------------------------------------------------

CREATE TABLE StockCode (
    id INT NOT NULL AUTO_INCREMENT,
    code VARCHAR(16),
    name VARCHAR(32),
    isin_code VARCHAR(16),
    listed_date DATETIME,
    market_type VARCHAR(16),
    industry_type VARCHAR(32),
    cfi_code VARCHAR(16),
    crawled_at DATETIME DEFAULT now(),
    created_at DATETIME DEFAULT now(),
    updated_at DATETIME DEFAULT now() ON UPDATE now(),
    PRIMARY KEY (id)
);


CREATE TABLE DateFrame (
    id INT NOT NULL,
    name VARCHAR(16),
    PRIMARY KEY (id),
    UNIQUE (name)
);


CREATE TABLE FinancialStatement (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(16),
    title VARCHAR(32),
    date_frame_id INT,
    is_snapshot BOOLEAN,
    is_consolidated BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (date_frame_id) REFERENCES DateFrame(id),
    UNIQUE (title)
);


CREATE TABLE FinancialStatementEntry (
    id INT NOT NULL AUTO_INCREMENT,
    statement_id INT,
    statement_date DATETIME,
    stock_code VARCHAR(16),
    metric_index INT,
    metric_name VARCHAR(32),
    metric_value DOUBLE,
    crawled_at DATETIME DEFAULT now(),
    created_at DATETIME DEFAULT now(),
    updated_at DATETIME DEFAULT now() ON UPDATE now(),
    PRIMARY KEY (id),
    FOREIGN KEY (statement_id) REFERENCES FinancialStatement(id)
);

-- -----------------------------------------------------------------------------

INSERT INTO DateFrame
    (id, name)
VALUES
    (0, 'Yearly'),
    (1, 'Quarterly'),
    (2, 'Monthly'),
    (3, 'Biweekly'),
    (4, 'Weekly'),
    (5, 'Daily');
