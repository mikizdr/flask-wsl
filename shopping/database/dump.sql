BEGIN TRANSACTION;
CREATE TABLE categories (
	id INTEGER NOT NULL,
	name VARCHAR(100) NOT NULL,
	description VARCHAR(500) NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	PRIMARY KEY (id)
);
INSERT INTO "categories"
VALUES(
		1,
		'Vegetable',
		'Different types of vegetables',
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36'
	);
INSERT INTO "categories"
VALUES(
		2,
		'Fruit',
		'Different types of fruits',
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36'
	);
INSERT INTO "categories"
VALUES(
		3,
		'Cereals',
		'Different types of cereals',
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36'
	);
CREATE TABLE products (
	id INTEGER NOT NULL,
	name VARCHAR(100) NOT NULL,
	description VARCHAR(1000) NOT NULL,
	price FLOAT NOT NULL,
	stock INTEGER NOT NULL,
	img_url VARCHAR(500) NOT NULL,
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
	images VARCHAR(500),
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
INSERT INTO "roles"
VALUES(
		1,
		'Admin',
		'Administrator',
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36'
	);
INSERT INTO "roles"
VALUES(
		2,
		'Seller',
		'Customer who sells product',
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36'
	);
INSERT INTO "roles"
VALUES(
		3,
		'Buyer',
		'Customer who buys products',
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36'
	);
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
INSERT INTO "users"
VALUES(
		1,
		'admin',
		'admin@email.com',
		NULL,
		'scrypt:32768:8:1$kRDbUYPHZ9Rotv8h$7bca717213f38ae943844dded3187d74f0099705d67bf79092b7ddcd08de1d2edc64cdba4cf43b3f2829b4dc473641462645c9b12af3bcadde935bb0e75414d8',
		NULL,
		'2024-03-06 15:18:36',
		'2024-03-06 15:18:36',
		1
	);
COMMIT;