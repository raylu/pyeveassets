#!/usr/bin/env python3

import requests

import db

def main():
	rs = requests.Session()
	rs.headers.update({'User-Agent': 'pyeveassets'})
	r = rs.get('https://esi.tech.ccp.is/v1/markets/prices/')
	r.raise_for_status()

	data = r.json()
	prices = []
	for item in data:
		price = item.get('average_price')
		if price:
			price = int(price * 100)
			prices.append((item['type_id'], price))
	db.update_prices(prices)

if __name__ == '__main__':
	main()
