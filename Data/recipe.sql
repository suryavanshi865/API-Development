
-- this is the Schema 
USE recipe;

DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cuisine VARCHAR(100),
    title VARCHAR(255),
    rating FLOAT NULL,
    prep_time INT NULL,
    cook_time INT NULL,
    total_time INT NULL,
    description TEXT,
    nutrients TEXT,
    serves VARCHAR(50)
);

DESCRIBE recipes;


