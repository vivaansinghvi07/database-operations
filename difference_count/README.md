# Difference Count

Includes scripts that count differences betewen a table in the Dev Database and the same in the Stage Database.

## Discrepancy Counter

The code for this version is in `count_discrepancies.py`. By putting entries into a dictionary based on the primary key of the table, it counts up the number of entries that are present in one table and not the other, then counts the number of rows which are not the same between tables.

## Row Count Differences

The code for this version is in `row_count_difference.py`. It simply determines the difference in the number of entries between a table in the Dev Database and the same in the Stage Database. 

