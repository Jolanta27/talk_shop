# Talk Shop

Talk Shop is a command-line shop assistant. Product data is stored persistently in a local SQLite database (`talk_shop.db`). On its first run, the application creates the database and adds the sample products.

## Requirements

- Python 3.13 or newer
- Project dependencies: Lark and SQLAlchemy

Install the project and dependencies with `py -m uv sync`, then start it with:

```powershell
py -m uv run talk-shop
```

The database file is created in the current working directory. Keep this file to retain products between runs.

## Application modes

At startup, choose user chat or administrator mode. In user mode, ask questions such as `How much is the monorail?`. Type `back` to return to the main menu. Product lookups use the current database contents.

The administrator menu provides:

1. Add product
2. Find product
3. Change product
4. Delete product
5. List products
6. Clear database

For add and change, enter the product name, price, and stock when prompted. Clearing the database requires typing `CLEAR` at the confirmation prompt. Cleared data remains cleared after restarting the application.

In the administrator menu, choose `0` to return to the main menu. In user chat, ask questions such as `How much is the monorail?` and type `back` to return.