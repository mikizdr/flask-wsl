BEGIN TRANSACTION;
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(500) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "categories" VALUES(1,'Vegetable','Different types of vegetables','2024-03-04 22:01:30','2024-03-04 22:01:30');
INSERT INTO "categories" VALUES(2,'Fruit','Different types of fruits','2024-03-04 22:01:30','2024-03-04 22:01:30');
INSERT INTO "categories" VALUES(3,'Cereals','Different types of cereals','2024-03-04 22:01:30','2024-03-04 22:01:30');
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(100), 
	description VARCHAR(1000), 
	price FLOAT, 
	stock INTEGER, 
	img_url VARCHAR(500), 
	category_id INTEGER, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
CREATE TABLE profiles (
	id INTEGER NOT NULL, 
	first_name VARCHAR(30), 
	last_name VARCHAR(30), 
	genre VARCHAR(1), 
	about VARCHAR(1000), 
	has_license BOOLEAN, 
	img_url VARCHAR(300), 
	phone VARCHAR(15), 
	address VARCHAR(100), 
	city VARCHAR(30), 
	zipcode VARCHAR(10), 
	country VARCHAR(30), 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR(20) NOT NULL, 
	description VARCHAR(1000), 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO "roles" VALUES(1,'Admin','Administrator','2024-03-04 22:01:30','2024-03-04 22:01:30');
INSERT INTO "roles" VALUES(2,'Seller','Customer who sells product','2024-03-04 22:01:30','2024-03-04 22:01:30');
INSERT INTO "roles" VALUES(3,'Buyer','Customer who buys products','2024-03-04 22:01:30','2024-03-04 22:01:30');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(30) NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	email_verified_at DATETIME, 
	password VARCHAR(60) NOT NULL, 
	remember_token VARCHAR(100), 
	role_id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);
-- admin password: admin
INSERT INTO "users" VALUES(1,'admin','admin@email.com',NULL,'scrypt:32768:8:1$zi3XOkkmJMmaYoT0$fd38151cbfdf95c549a04367ef876a35b3084e3e0526e4b6f704f6f9450043a189dbc008c97c1013c56470e2f7ab7a95de1a4a69b85d1294c7c0c2e3e0cc211b',NULL,1,'2024-03-04 22:01:30','2024-03-04 22:01:30');
COMMIT;
