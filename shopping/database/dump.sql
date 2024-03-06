BEGIN TRANSACTION;
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(500) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "categories" VALUES(1,'Vegetable','Different types of vegetables','2024-03-06 16:22:07','2024-03-06 16:22:07');
INSERT INTO "categories" VALUES(2,'Fruit','Different types of fruits','2024-03-06 16:22:07','2024-03-06 16:22:07');
INSERT INTO "categories" VALUES(3,'Cereals','Different types of cereals','2024-03-06 16:22:07','2024-03-06 16:22:07');
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(1000) NOT NULL, 
	price FLOAT NOT NULL, 
	stock INTEGER NOT NULL, 
	images VARCHAR(500) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	category_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE profiles (
	id INTEGER NOT NULL, 
	first_name VARCHAR(30), 
	last_name VARCHAR(30), 
	genre VARCHAR(1), 
	about VARCHAR(1000), 
	has_license BOOLEAN, 
	profile_img VARCHAR(500), 
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
INSERT INTO "roles" VALUES(1,'Admin','Administrator','2024-03-06 16:22:07','2024-03-06 16:22:07');
INSERT INTO "roles" VALUES(2,'Seller','Customer who sells product','2024-03-06 16:22:07','2024-03-06 16:22:07');
INSERT INTO "roles" VALUES(3,'Buyer','Customer who buys products','2024-03-06 16:22:07','2024-03-06 16:22:07');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(30) NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	email_verified_at DATETIME, 
	password VARCHAR(60) NOT NULL, 
	remember_token VARCHAR(100), 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);
INSERT INTO "users" VALUES(1,'admin','admin@email.com',NULL,'scrypt:32768:8:1$p8ADYi7jKC6Tw8ET$65155852228e05aa68cf1ffc2c3164a069172dc23bfd4aff790657501c3c27dbf2f24a2593c548bb41b87563080f02f6f2afc679a0a2d1f6deff9feafbcca1ff',NULL,'2024-03-06 16:22:07','2024-03-06 16:22:07',1);
COMMIT;
