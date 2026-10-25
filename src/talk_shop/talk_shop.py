from lark import Lark, Token, Tree
from lark.exceptions import LarkError

from .data_shop import Product, ProductDatabase


grammar = """
%import common.WS
%ignore WS

start: price_question

price_question: HOW_MUCH BE DET ITEM "?"? | HOW_MUCH BE ITEM "?"?

HOW_MUCH: "how much"
BE: "is" | "are"
DET: "the" | "a" | "any"
ITEM: /[a-z]+(?: [a-z]+)*/
"""


def process_query(query: str, database: ProductDatabase | None = None) -> str:
	product_database = database or ProductDatabase()
	try:
		tree = Lark(grammar, parser="earley").parse(query.lower().strip())
	except LarkError:
		return "Unable to process query. Try: How much is the monorail?"

	query_node: Tree | Token = tree.children[0]
	if not isinstance(query_node, Tree) or query_node.data != "price_question":
		return "Unable to process query."

	item = next(query_node.find_token("ITEM"), None)
	if not isinstance(item, Token):
		return "Unable to process query."

	product = product_database.find_product(str(item))
	if product is None:
		return f"Sorry, I couldn't find {item}."
	return f"The {product.name} costs ${product.price:.2f}."


def _read_product() -> Product:
	name = input("Product name: ").strip()
	price = float(input("Price: "))
	stock = int(input("Stock: "))
	return Product(name, price, stock)


def admin_menu(database: ProductDatabase) -> None:
	while True:
		print("\nADMIN MENU")
		print("1 - Add product")
		print("2 - Find product")
		print("3 - Change product")
		print("4 - Delete product")
		print("5 - List products")
		print("6 - Clear database")
		print("0 - Back")
		choice = input("Choose an option: ").strip()

		try:
			if choice == "1":
				database.add_product(_read_product())
				print("Product added.")
			elif choice == "2":
				product = database.find_product(input("Product name: "))
				print(_format_product(product) if product else "Product not found.")
			elif choice == "3":
				identifier = input("Product name to change: ")
				product = _read_product()
				print("Product updated." if database.update_product(identifier, product) else "Product not found.")
			elif choice == "4":
				identifier = input("Product name to delete: ")
				print("Product deleted." if database.delete_product(identifier) else "Product not found.")
			elif choice == "5":
				_format_products(database.list_products())
			elif choice == "6":
				confirmation = input("Type CLEAR to delete every product: ")
				if confirmation == "CLEAR":
					database.clear()
					print("Database cleared.")
				else:
					print("Clear cancelled.")
			elif choice == "0":
				return
			else:
				print("Choose an option from 0 to 6.")
		except (ValueError, TypeError) as error:
			print(f"Invalid product data: {error}")


def _format_product(product: Product) -> str:
	return f"{product.name} | ${product.price:.2f} | stock: {product.stock}"


def _format_products(products: list[Product]) -> None:
	print(f"\nProducts in database ({len(products)}):")
	if not products:
		print("No products in the database.")
		return
	for product in products:
		print(_format_product(product))


def user_chat(database: ProductDatabase) -> None:
	print("Ask about a product price. Type 'back' to return to the main menu.")
	while True:
		query = input("Query: ").strip()
		if query.lower() in {"back", "exit", "quit"}:
			return
		print(process_query(query, database))


def main() -> None:
	database = ProductDatabase()
	while True:
		print("\nTALK SHOP")
		print("1 - User chat")
		print("2 - Administrator")
		print("0 - Exit")
		choice = input("Choose a mode: ").strip()
		if choice == "1":
			user_chat(database)
		elif choice == "2":
			admin_menu(database)
		elif choice == "0":
			return
		else:
			print("Choose 1, 2, or 0.")


if __name__ == "__main__":
	main()