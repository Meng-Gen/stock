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
    name = Column(String(8), unique=True)


class FinancialStatement(Base):
    __tablename__ = 'FinancialStatement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    title = Column(String(32), unique=True)
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


class StockPrice(Base):
    __tablename__ = 'StockPrice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(16))
    date = Column(DateTime())
    volume = Column(Float(53))
    open = Column(Float(53))
    high = Column(Float(53))
    low = Column(Float(53))
    close = Column(Float(53))
    crawled_at = Column(DateTime(), server_default=func.now())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


class StockCodeStore():
    """A store to manipulate StockCode table in the stock database.

    Use SQLAlchemy ORM to manipulate StockCode table in the stock database.
    """

    def get(self):
        session = Session()
        results = session.query(StockCode.code).filter(StockCode.id.in_(
            session.query(func.max(StockCode.id)).filter_by(cfi_code='ESVUFR').group_by(StockCode.code))
        )
        stock_codes = [entry.code for entry in results]
        session.close()
        return stock_codes


class DateFrameStore():
    """A store to manipulate DateFrame table in MySQL database.

    Use SQLAlchemy ORM to manipulate DateFrame table in the stock database.
    """

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

    def get(self, name):
        return self.cached_ids[name]


class FinancialStatementEntryStore():
    pass


class StockPriceStore():
    pass