from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('mysql+mysqldb://stockcats:stockcats@localhost/stockcats?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine)


class StockCode(Base):
    __tablename__ = 'StockCode'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(16))
    name = Column(String(32))
    isin_code = Column(String(16))
    listed_date = Column(DateTime())
    market_type = Column(String(16))
    industry_type = Column(String(32))
    cfi_code = Column(String(16))
    crawled_at = Column(DateTime(), server_default=func.now())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


class DateFrame(Base):
    __tablename__ = 'DateFrame'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(8))


class FinancialStatement(Base):
    __tablename__ = 'FinancialStatement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    date_frame_id = Column(Integer, ForeignKey("DateFrame.id"), nullable=False)
    is_snapshot = Column(Boolean)
    is_consolidated = Column(Boolean)


class FinancialStatementEntry(Base):
    __tablename__ = 'FinancialStatementEntry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    statement_id = Column(Integer, ForeignKey("FinancialStatement.id"), nullable=False)
    statement_date = Column(DateTime())
    stock_code = Column(String(16))
    metric_index = Column(Integer)
    metric_name = Column(String(32))
    metric_value = Column(Float(53))


class StockCodeStore():
    """A store to manipulate StockCode table in the stock database.

    We leverage SQLAlchemy ORM to manipulate StockCode table in the stock
    database (MySQL).
    """

    cached_items = []

    def add(self, item):
        """Add a StockCodeItem into cached items.

        Add a StockCodeItem into the list of cached items. Call flush() method
        to persist all cached items.

        Args:
            item: A StockCodeItem
        """
        self.cached_items.append(item)

    def flush(self):
        """Flush all cached items into MySQL database.

        Flush all cached items into MySQL database and clear all cached items.
        """
        session = Session()
        for item in self.cached_items:
            session.add(self._build_item(item))
        session.commit()
        session.close()
        del self.cached_items[:]

    def _build_item(self, item):
        """Build a StockCode from a StockCodeItem.

        Build a StockCode from a StockCodeItem to adapt SQLAlchemy ORM.

        Args:
            item: A StockCodeItem

        Returns:
            A StockCode instance (SQLAlchemy ORM)
        """
        return StockCode(
            code=item['code'], 
            name=item['name'],
            isin_code=item['isin_code'],
            listed_date=item['listed_date'],
            market_type=item['market_type'],
            industry_type=item['industry_type'],
            cfi_code=item['cfi_code']
        )


class FinancialStatementEntryStore():
    """A store to manipulate FinancialStatementEntry table in MySQL database.

    We leverage SQLAlchemy ORM to manipulate FinancialStatementEntry table in
    the stock database (MySQL).
    """
    cached_items = []

    def add(self, item):
        """Add a FinancialStatementEntryItem into cached items.

        Add a FinancialStatementEntryItem into the list of cached items. Call
        flush() method to persist all cached items.

        Args:
            item: A FinancialStatementEntryItem
        """
        self.cached_items.append(item)

    def flush(self):
        session = Session()
        #for item in self.cached_items:
        #    session.add(self._build_item(item))
        #session.commit()
        session.close()
        del self.cached_items[:]

    def _build_item(self, item):
        """Build a FinancialStatementEntry from a FinancialStatementEntryItem.

        Build a FinancialStatementEntry from a FinancialStatementEntryItem to
        adapt SQLAlchemy ORM.

        Args:
            item: A FinancialStatementEntryItem

        Returns:
            A FinancialStatementEntry instance (SQLAlchemy ORM)
        """
        pass