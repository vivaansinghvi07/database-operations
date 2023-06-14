''' 
Counts the number of discrepancies between two tables.
The method used:
	- Count the number of entries in each table that are not in the other (by primary key).
	- For rows that exist in both tables, count the number of rows that are different.
	- Create detailed logs if necessary.
''' 

import sys
from pathlib import Path
from typing import List
from time import perf_counter
from colorama import Fore, Style

DIR_PATH = str(Path(__file__).parent)
sys.path.append(f"{DIR_PATH}/..")

from database import Database

''' 
Tab pattern for logging:
0 tabs for table
	1 tab for row differences
		2 tabs for each item
'''

def h_print(prompt: str, end: None = "\n"):
	''' print method override for highlighted text '''
	print(f"{Style.BRIGHT}{prompt}{Style.RESET_ALL}", end=end)	

def get_differences(dev_row, stage_row, colnames):
	''' Returns a string describing the differences in a row. ''' 
	output = f"\trow with {colnames[0]} '{dev_row[0]}': \n" # will be the primary key
	differences: List[str] = [] 
	for name, dev_item, stage_item in zip(colnames, dev_row, stage_row):
		if dev_item != stage_item:
			differences.append(f"\t\tdifference in column '{name}':: dev: '{dev_item}', stage: '{stage_item}'\n")
	return output + "".join(differences)

def check_table_differences(table: str, log_differences: bool) -> int:	

	# loads the database information into two dictionaries
	with Database("Stage Database")  as stage, Database("Dev Database") as dev:
		primary_key_count = len(dev.prim_keys(table))
		if primary_key_count == 0:
			h_print(f"{Fore.RED}ALERT:{Fore.RESET} No primary keys found for table {Fore.GREEN}'{table}'{Fore.RESET}. Defaulting to the first column.") 
			primary_key_count = 1

		stage_rows, dev_rows = {}, {}
		stage.query(f"SELECT * FROM {table}")
		dev.query(f"SELECT * FROM {table}")

		for row in dev:
			row = tuple(map(str, row))
			dev_rows[row[:primary_key_count]] = row
		for row in stage:
			row = tuple(map(str, row))
			stage_rows[row[:primary_key_count]] = row
		colnames = dev.colnames(table)
	
	# obtains the keys and initializes logger
	stage_keys, dev_keys = {*stage_rows}, {*dev_rows}	
	differences: List[str] = []
	
	# determines entries exclusive to either table
	dev_not_stage = len(dev_keys - stage_keys)
	stage_not_dev = len(stage_keys - dev_keys)
	if log_differences and dev_not_stage > 0: 
		differences.append(f"\t{dev_not_stage} entries exist in 'dev' that do not in 'stage'.\n")
	if log_differences and stage_not_dev > 0:
		differences.append(f"\t{stage_not_dev} entries exist in 'stage' that do not in 'dev'.\n")
	difference_count = dev_not_stage + stage_not_dev	

	# adds up differences for similar rows
	for key in stage_keys & dev_keys:
		is_diff = stage_rows[key] != dev_rows[key]
		difference_count += int(is_diff)
		if is_diff and log_differences:
			differences.append(get_differences(stage_rows[key], dev_rows[key], colnames))
	
	# writes differences in file
	if log_differences:
		with open(f"table_differences.txt", 'w', encoding='utf-8') as f:
			if difference_count > 0:
				f.write(f"Differences for table '{table}':\n")
				f.writelines(differences)
			else:
				f.write(f"No differences for table '{table}'.\n")

	return difference_count, len(stage_keys | dev_keys)

def main():
	args = sys.argv[1:]
	log_diffs = any([opt in args for opt in ['-l', '--log-differences']])
	for table in filter(lambda arg: arg[0]!='-', args):
		start = perf_counter()
		diff_count, entry_count = check_table_differences(table, log_diffs)
		time_taken = perf_counter() - start
		h_print(f"Number of differences for table {Fore.GREEN}'{table}'{Fore.RESET} was {Fore.BLUE}{diff_count}{Fore.RESET}. Analyzed {Fore.BLUE}{entry_count:,}{Fore.RESET} entries in {Fore.BLUE}{time_taken:.2f}{Fore.RESET} seconds.")

if __name__ == "__main__":
	main()
