# big-fiubrother-core

Big Fiubrother core utilities

# Scripts

Install shovel to run utility scripts. This can be achieved by running the following command:

```
python -m pip install shovel
```

## Database

### Setup

Creates postgresql database with entities. A postgresql server must be running in the target host before executing the script. Username and password are required.

```
shovel db.setup [username] [password] ([host=localhost] [database_name=big_fiubrother])
```

### Drop

Drops postgresql database. A postgresql server must be running in the target host before executing the script. Username and password are required.

```
shovel db.drop [username] [password] ([host=localhost] [database_name=big_fiubrother])
```