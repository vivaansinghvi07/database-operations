-- Gets the primary keys of a table given its schema and its name
SELECT DISTINCT ccu.column_name  
FROM information_schema.constraint_column_usage as ccu
JOIN information_schema.table_constraints tc ON tc.constraint_name = ccu.constraint_name
WHERE ccu.table_schema = '{}' AND ccu.table_name = '{}' AND constraint_type = 'PRIMARY KEY';
