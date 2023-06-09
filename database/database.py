import psycopg2
import configparser
import os
import sys
from pathlib import Path
from typing import List, Tuple

class Database:

	def __init__(self, dbname: str) -> None:

		# obtain credentials
		config = configparser.ConfigParser()
		config.read(f"{Path(__file__).parent}/creds.ini")
		creds = dict(config[dbname].items())

		self.conn = psycopg2.connect(**creds)
		self.cur = self.conn.cursor()
	
	def end(self) -> None:
		self.conn.commit()
		self.conn.close()

	def __enter__(self):
		return self

	def __exit__(self, *args) -> None:
		self.end()
	
	def query(self, prompt: str) -> None:
		self.cur.execute(prompt)

	def fetchall(self) -> List[Tuple[str]]:
		return self.cur.fetchall()

	def colnames(self, table: str) -> List[str]:
		self.cur.execute(f"SELECT * FROM {table} LIMIT 0")
		return [desc[0] for desc in self.cur.description]
		
	def prim_keys(self, table: str) -> List[str]:
		with open(f"{Path(__file__).parent}/primary_key.sql", 'r') as f:
			qu = f.read().format(*table.split('.'))
		self.cur.execute(qu)
		return [item[0] for item in self.fetchall()]

	def __iter__(self):
		return self

	def __next__(self):
		output = self.cur.fetchone()
		if output is None:
			raise StopIteration
		return output
	
if __name__ == "__main__":
	dev = Database("Dev Database")
	stage = Database("Stage Database")

