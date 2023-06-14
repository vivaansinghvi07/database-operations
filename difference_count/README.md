# Difference Count

Includes scripts that count differences betewen a table in the Dev Database and the same in the Stage Database.

## Discrepancy Counter

The code for this version is in `count_discrepancies.py`. By putting entries into a dictionary based on the primary key of the table, it counts up the number of entries that are present in one table and not the other, then counts the number of rows which are not the same between tables. This version also supports logging, if you want to know and keep track of each discrepancy for later reference.

To run this, run the following shell script:
```
$ python3 count_discrepancies.py --log-differences <schema1>.<table1> <schema2>.<table2> ...
```

`--log-differences`, or `-l` for short, determines if the differences will be logged in a file called `table_differences.txt`, located in whichever directory the script is called from.

Each table is entered with its corresponding schema, replacing `<table>` and `<schema>` respectively.

## Row Count Differences

The code for this version is in `row_count_difference.py`. It simply determines the difference in the number of entries between a table in the Dev Database and the same in the Stage Database. 

To run this, run the following shell script:
```
$ python3 row_count_difference.py <schema1>.<table1> <schema2>.<table2> ...
```

Again, each table is entered with its corresponding schema, replacing `<table>` and `<schema>` respectively.
