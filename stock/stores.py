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

    Use SQLAlchemy ORM to manipulate StockCode table in the stock database.
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


class DateFrameStore():
    """A store to manipulate DateFrame table in MySQL database.

    Use SQLAlchemy ORM to manipulate DateFrame table in the stock database.
    """

    ACCEPTED_STATEMENT_TITLE_MAP = {
        # consolidated balance sheet (yearly)
        u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u5e74\u8868': 'Yearly',
        # consolidated balance sheet (quarterly)
        u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u8ca1\u5831\u5b63\u8868': 'Quarterly',
    }

    cached_ids = {}

    def __init__(self):
        """Init cached_ids map.

        Init cached_ids map by DateFrame table. Each record of DateFrame has
        the id and the corresponding name, and we map each name to the unique
        id as a cached record.
        """
        session = Session()
        for entry in session.query(DateFrame):
            self.cached_ids[entry.name] = entry.id
        session.close()

    def get_id(self, statement_title):
        """Get id (foreign key) of DateFrame from statement title.

        Get the id of DateFrame from the specific title of the financial
        statement. All records of DateFrame table are prepared.

        Args:
            statement_title: A title of the financial statement.

        Returns:
            An integer id representing the date frame of the financial
            statement.

        Raises:
            ValueError: An error occurred parsing the date frame.
        """
        if statement_title in ACCEPTED_STATEMENT_TITLE_MAP:
            return self.cached_ids[ACCEPTED_STATEMENT_TITLE_MAP[statement_title]]
        else:
            raise ValueError(u'Could not parse date frame: {0}'.format(statement_title))


class FinancialStatementStore():
    """A store to manipulate FinancialStatement table in MySQL database.

    Use SQLAlchemy ORM to manipulate FinancialStatement table in the stock
    database.
    """

    ACCEPTED_STATEMENT_TITLE_LIST = [
        # consolidated balance sheet (yearly)
        u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u5e74\u8868',
        # consolidated balance sheet (quarterly)
        u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u8ca1\u5831\u5b63\u8868',
    ]

    cached_ids = {}

    date_frame_store = DateFrameStore()

    def __init__(self):
        self._init_cached_ids()

    def get_id(self, statement_title):
        """Get id (foreign key) of FinancialStatement from statement title.

        Get id of FinancialStatement from the specific title of the financial
        statement. If id is not in the FinancialStatement table, insert a new
        record representing an accepted title of a financial statement.

        Args:
            statement_title: A title of the financial statement.

        Returns:
            An integer id representing the financial statement.

        Raises:
            ValueError: An error occurred parsing the statement id.
        """
        if statement_title not in self.cached_ids:
            if statement_title in ACCEPTED_STATEMENT_TITLE_LIST:
                session = Session()
                session.add(FinancialStatement(
                    name=statement_title,
                    date_frame_id=self.date_frame_store.get_id(statement_title),
                    is_snapshot=True,
                    is_consolidated=True
                ))
                session.commit()
                session.close()
                self._init_cached_ids()
            else:
                raise ValueError(u'Could not parse statement id: {0}'.format(statement_title))
        return self.cached_ids[statement_title]

    def _init_cached_ids(self):
        """Init cached_ids map.

        Init cached_ids map by FinancialStatement table. Each record of
        FinancialStatement has the id and the corresponding name, and we map
        each name to the unique id as a cached record.
        """
        self.cached_ids.clear()

        session = Session()
        for entry in session.query(FinancialStatement):
            self.cached_ids[entry.name] = entry.id
        session.close()


class FinancialStatementEntryStore():
    """A store to manipulate FinancialStatementEntry table in MySQL database.

    Use SQLAlchemy ORM to manipulate FinancialStatementEntry table in the stock
    database.
    """

    cached_items = []

    financial_statement_store = FinancialStatementStore()

    def add(self, item):
        """Add a FinancialStatementEntryItem into cached items.

        Add a FinancialStatementEntryItem into the list of cached items. Call
        flush() method to persist all cached items.

        Args:
            item: A FinancialStatementEntryItem
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
        """Build a FinancialStatementEntry from a FinancialStatementEntryItem.

        Build a FinancialStatementEntry from a FinancialStatementEntryItem to
        adapt SQLAlchemy ORM.

        Args:
            item: A FinancialStatementEntryItem

        Returns:
            A FinancialStatementEntry instance (SQLAlchemy ORM)
        """
        return FinancialStatementEntry(
            statement_id=self.financial_statement_store.get_id(item['title']),
            statement_date=item['statement_date'],
            stock_code=item['stock_code'],
            metric_index=item['metric_index'],
            metric_name=item['metric_name'],
            metric_value=item['metric_value']
        )
