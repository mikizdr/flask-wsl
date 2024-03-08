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
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
INSERT INTO "categories"
VALUES(
		2,
		'Fruit',
		'Different types of fruits',
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
INSERT INTO "categories"
VALUES(
		3,
		'Cereals',
		'Different types of cereals',
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
CREATE TABLE products (
	id INTEGER NOT NULL,
	name VARCHAR(100) NOT NULL,
	description VARCHAR(1000) NOT NULL,
	price FLOAT NOT NULL,
	stock INTEGER NOT NULL,
	images VARCHAR(500) NOT NULL,
	category_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
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
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
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
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
INSERT INTO "roles"
VALUES(
		2,
		'Seller',
		'Customer who sells product',
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
INSERT INTO "roles"
VALUES(
		3,
		'Buyer',
		'Customer who buys products',
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
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
INSERT INTO "users"
VALUES(
		1,
		'admin',
		'admin@email.com',
		NULL,
		'scrypt:32768:8:1$uYtXHqCmBf0jC58v$4dad39c1c1a291b9538b00afd64ee35317074d347416dcd598bc2026ddc3be3d7b034b1cf1b0bd58ad5a0761a01cf799bb8cacbd4f14ad5c2cfc9749d8fdcb6b',
		NULL,
		1,
		'2024-03-08 21:45:23',
		'2024-03-08 21:45:23'
	);
CREATE TABLE users_products (
	user_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	PRIMARY KEY (user_id, product_id),
	FOREIGN KEY(user_id) REFERENCES users (id),
	FOREIGN KEY(product_id) REFERENCES products (id)
);
COMMIT;