''' Determines the difference in row counts between the two tables '''
import sys
from pathlib import Path

DIR_PATH = Path(__file__).parent
sys.path.append(f'{DIR_PATH}/..')

from database import Database
from colorama import Fore, Style

def calculate_difference(table: str) -> int:
	with Database("Dev Database") as dev, Database("Stage Database") as stage:
		dev.query(f"SELECT COUNT(*) FROM {table}")
		stage.query(f"SELECT COUNT(*) FROM {table}")
		return dev.fetchall()[0][0] - stage.fetchall()[0][0]

def main():
	for table in sys.argv[1:]:
		diff = calculate_difference(table)
		if diff == 0: output = f"the {Fore.BLUE}same{Fore.RESET} amount of entries as"
		else: output = f"{Fore.BLUE}{abs(diff):,}{Fore.RESET} {'more' if diff > 0 else 'less'} entries than"
		print(f"{Style.BRIGHT}The dev database has {output} the stage database for table {Fore.GREEN}'{table}'{Fore.RESET}{Style.RESET_ALL}.") 
	
if __name__ == "__main__":
	main()
