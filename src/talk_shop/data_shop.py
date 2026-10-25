from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import Float, Integer, String, create_engine, inspect, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
	pass


class ProductRecord(Base):
	__tablename__ = "products"

	product_id: Mapped[str] = mapped_column(String, primary_key=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	price: Mapped[float] = mapped_column(Float, nullable=False)
	stock: Mapped[int] = mapped_column(Integer, nullable=False)


@dataclass(frozen=True)
class Product:
	name: str
	price: float
	stock: int


DEFAULT_PRODUCTS = (
	Product(name="Monorail", price=1449.99, stock=30),
	Product(name="Hewlett Packard", price=1849.99, stock=23),
	Product(name="COMPAQ", price=2399.99, stock=8),
)


def product_id(name: str) -> str:
	return "_".join(name.strip().lower().split())


class ProductDatabase:
	def __init__(self, path: str | Path = "talk_shop.db") -> None:
		self.engine = self._create_engine(path)
		table_exists = inspect(self.engine).has_table("products")
		Base.metadata.create_all(self.engine)
		if not table_exists:
			with Session(self.engine) as session:
				session.add_all(self._record(item) for item in DEFAULT_PRODUCTS)
				session.commit()

	@staticmethod
	def _create_engine(path: str | Path) -> Engine:
		if str(path) == ":memory:":
			return create_engine("sqlite+pysqlite:///:memory:")
		database_path = Path(path)
		database_path.parent.mkdir(parents=True, exist_ok=True)
		return create_engine(f"sqlite+pysqlite:///{database_path.resolve().as_posix()}")

	@staticmethod
	def _record(product: Product) -> ProductRecord:
		return ProductRecord(
			product_id=product_id(product.name),
			name=product.name.strip(),
			price=product.price,
			stock=product.stock,
		)

	@staticmethod
	def _product(record: ProductRecord) -> Product:
		return Product(record.name, record.price, record.stock)

	@staticmethod
	def _validate(product: Product) -> None:
		if not product.name.strip():
			raise ValueError("Product name cannot be empty.")
		if product.price < 0:
			raise ValueError("Price cannot be negative.")
		if product.stock < 0:
			raise ValueError("Stock cannot be negative.")

	def list_products(self) -> list[Product]:
		with Session(self.engine) as session:
			records = session.scalars(select(ProductRecord).order_by(ProductRecord.name)).all()
			return [self._product(record) for record in records]

	def find_product(self, identifier: str) -> Product | None:
		with Session(self.engine) as session:
			record = session.scalar(
				select(ProductRecord).where(
					(ProductRecord.product_id == product_id(identifier))
					| (ProductRecord.name.ilike(identifier.strip()))
				)
			)
			return self._product(record) if record else None

	def add_product(self, product: Product) -> None:
		self._validate(product)
		with Session(self.engine) as session:
			if session.get(ProductRecord, product_id(product.name)):
				raise ValueError("Product with this name already exists.")
			session.add(self._record(product))
			session.commit()

	def update_product(self, identifier: str, product: Product) -> bool:
		self._validate(product)
		with Session(self.engine) as session:
			record = session.scalar(
				select(ProductRecord).where(
					(ProductRecord.product_id == product_id(identifier))
					| (ProductRecord.name.ilike(identifier.strip()))
				)
			)
			if record is None:
				return False
			new_id = product_id(product.name)
			if new_id != record.product_id and session.get(ProductRecord, new_id):
				raise ValueError("Product with this name already exists.")
			record.product_id = new_id
			record.name = product.name.strip()
			record.price = product.price
			record.stock = product.stock
			session.commit()
			return True

	def delete_product(self, identifier: str) -> bool:
		with Session(self.engine) as session:
			record = session.scalar(
				select(ProductRecord).where(
					(ProductRecord.product_id == product_id(identifier))
					| (ProductRecord.name.ilike(identifier.strip()))
				)                $env:Path += ";$env:LOCALAPPDATA\Programs\Git\cmd"
                git --version
                git status
			)
			if record is None:
				return False
			session.delete(record)
			session.commit()
			return True

	def clear(self) -> None:
		with Session(self.engine) as session:
			session.query(ProductRecord).delete()
			session.commit()