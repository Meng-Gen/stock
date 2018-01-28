from sqlalchemy import Column
from sqlalchemy import DateTime
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
    

class StockCodeStore():
    cached_items = []

    def add(self, item):
        """
        Args:
            item: A stock.items.StockCodeItem
        """
        self.cached_items.append(item)

    def flush(self):
        session = Session()
        for item in self.cached_items:
            session.add(self._build_item(item))
        session.commit()
        session.close()
        del self.cached_items[:]

    def _build_item(self, item):
        return StockCode(
            code=item['code'], 
            name=item['name'],
            isin_code=item['isin_code'],
            listed_date=item['listed_date'],
            market_type=item['market_type'],
            industry_type=item['industry_type'],
            cfi_code=item['cfi_code']
        )