import sys
sys.path.append('..')

from database import Database
from typing import List

''' 
Tab pattern for logging:
0 tabs for table
	1 tab for row differences
		2 tabs for each item
'''

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
			print(f"No primary keys found for table '{table}'. Defaulting to the first column.") 
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
		differences.append(f"{dev_not_stage} entries exist in 'dev' that do not in 'stage'.")
	if log_differences and stage_not_dev > 0:
		differences.append(f"{stage_not_dev} entries exist in 'stage' that do not in 'dev'.")
	difference_count = dev_not_stage + stage_not_dev	

	# adds up differences for similar rows
	for key in stage_keys & dev_keys:
		is_diff = stage_rows[key] != dev_rows[key]
		difference_count += int(is_diff)
		if is_diff and log_differences:
			differences.append(get_differences(stage_rows[key], dev_rows[key], colnames))
	
	# writes differences in file
	if log_differences:
		with open("table_differences.txt", 'w', encoding='utf-8') as f:
			if difference_count > 0:
				f.write(f"Differences for table \"{table}\":\n")
				f.writelines(differences)
			else:
				f.write(f"No differences for table \"{table}\".\n")

	return difference_count

def main():
	args = sys.argv[1:]
	log_diffs = any([opt in args for opt in ['-l', '--log-differences']])
	for table in filter(lambda arg: arg[0]!='-', args):
		diff_count = check_table_differences(table, log_diffs)
		print(f"Number of differences for table \"{table}\" was {diff_count}.")

if __name__ == "__main__":
	main()
