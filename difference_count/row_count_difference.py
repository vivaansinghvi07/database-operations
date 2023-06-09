''' Determines the difference in row counts between the two tables '''
import sys
sys.path.append('..')

from database import Database

def calculate_difference(table: str) -> int:
	with Database("Dev Database") as dev, Database("Stage Database") as stage:
		dev.query(f"SELECT COUNT(*) FROM {table}")
		stage.query(f"SELECT COUNT(*) FROM {table}")
		return dev.fetchall()[0][0] - stage.fetchall()[0][0]

def main():
	for table in sys.argv[1:]:
		diff = calculate_difference(table)
		if diff == 0: output = "the same amount of entries as"
		else: output = f"{abs(diff)} {'more' if diff > 0 else 'less'} entries than"
		print(f"The dev database has {output} the stage database for table '{table}'.") 

if __name__ == "__main__":
	main()
