DROP TABLE IF EXISTS "eve_characters";
DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
	"user_id" serial PRIMARY KEY,
	"username" varchar(32) NOT NULL,
	"password" varchar(120) NOT NULL,
	UNIQUE("username")
);

CREATE TABLE "eve_characters" (
	"char_id" integer PRIMARY KEY,
	"user_id" integer NOT NULL REFERENCES "users" ("user_id"),
	"char_name" varchar(64) NOT NULL,
	"token" varchar(64) NOT NULL,
	"token_expires" timestamp NOT NULL,
	"refresh_token" varchar(64) NOT NULL
);
