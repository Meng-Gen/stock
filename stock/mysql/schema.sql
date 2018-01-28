DROP TABLE IF EXISTS StockCode;

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