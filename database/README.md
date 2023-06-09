# Database

Abstracts some database information away into a base class so that it can easily be called through other programs. To initialize a database, have configuration credentials in a `conf.ini` file, as shown below:


<details>
<summary>conf.ini</summary>

```ini
[DATABASE_NAME]
host=
port=
user=
password=
database=
```

`DATABASE_NAME` represents an arbitrary name of the database which you will call in a script. The rest of the information should be filled out depending on the database being accessed.

</details>

Then, you can simply call the following, assuming you have properly imported the `database` submodule. 

```python
from database import Database
DATABASE_NAME = "your_name_here"
db = Database(DATABASE_NAME)
```
Note that `DATABASE_NAME` should match its counterpart in the `conf.ini` file.

