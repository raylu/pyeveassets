DROP TABLE IF EXISTS "eve_chars";
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "item_prices";

CREATE TABLE "users" (
	"user_id" serial PRIMARY KEY,
	"username" varchar(32) NOT NULL,
	"password" varchar(120) NOT NULL,
	UNIQUE("username")
);

CREATE TABLE "eve_chars" (
	"char_id" integer PRIMARY KEY,
	"user_id" integer NOT NULL REFERENCES "users" ("user_id"),
	"char_name" varchar(64) NOT NULL,
	"token" varchar(128) NOT NULL,
	"token_expires" timestamp NOT NULL,
	"refresh_token" varchar(128) NOT NULL
);

CREATE TABLE "item_prices" (
	"type_id" serial PRIMARY KEY,
	"price" bigint NOT NULL
);
