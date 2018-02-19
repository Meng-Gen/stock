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

from time_series import TimeSeries


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
            session.query(func.max(StockCode.id)) \
                .filter_by(cfi_code='ESVUFR') \
                .group_by(StockCode.code)
            )
        )
        stock_codes = [entry.code for entry in results]
        session.close()
        return stock_codes


class FinancialStatementStore():
    """A store to manipulate FinancialStatement table in the stock database.

    Use SQLAlchemy ORM to manipulate FinancialStatement table joining with
    DateFrame table.
    """

    cached_date_frame_map = {}
    cached_is_snapshot_map = {}

    def __init__(self):
        session = Session()
        results = session.query(FinancialStatement.id, FinancialStatement.is_snapshot, DateFrame.name) \
            .join(DateFrame).all()
        self.cached_date_frame_map = dict([(entry.id, entry.name) for entry in results])
        self.cached_is_snapshot_map = dict([(entry.id, entry.is_snapshot) for entry in results])
        session.close()

    def get_date_frame(self, statement_id):
        return self.cached_date_frame_map[statement_id]

    def get_is_snapshot(self, statement_id):
        return self.cached_is_snapshot_map[statement_id]


class FinancialStatementEntryStore():
    """A store to manipulate FinancialStatementEntry table.

    Use SQLAlchemy ORM to manipulate FinancialStatementEntry table.
    """

    financial_statement_store = FinancialStatementStore()

    def get(self, metric_name):
        """Get metric values by metric names.

        Args:
            metric_name: A string of metric names.

        Returns:
            A map of TimeSeries. Keys are date frames and values are
            corresponding TimeSeries.
        """
        output = {}
        statement_ids = self._get_statement_ids_containing(metric_name)
        for statement_id in statement_ids:
            date_frame = self.financial_statement_store.get_date_frame(statement_id)
            is_snapshot = self.financial_statement_store.get_is_snapshot(statement_id)
            results = self._get_by_statement_id(metric_name, statement_id)
            dates = [entry.statement_date for entry in results]
            values = [entry.metric_value for entry in results]

            output[date_frame] = TimeSeries.create(
                date_frame=date_frame,
                is_snapshot=is_snapshot,
                dates=dates,
                values=values
            )
        return output

    def _get_statement_ids_containing(self, metric_name):
        session = Session()
        results = session.query(FinancialStatementEntry.statement_id).distinct().filter_by(metric_name=metric_name)
        statement_ids = [entry.statement_id for entry in results]
        session.close()
        return statement_ids

    def _get_by_statement_id(self, metric_name, statement_id):
        session = Session()
        results = session.query(FinancialStatementEntry).filter(FinancialStatementEntry.id.in_(
            session.query(func.max(FinancialStatementEntry.id)) \
                .filter_by(metric_name=metric_name) \
                .filter_by(statement_id=statement_id) \
                .group_by(FinancialStatementEntry.statement_date)
            )
        )
        session.close()
        return results


class StockPriceStore():
    pass