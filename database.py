from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "mysql+pymysql://root:981023@localhost/Project_E"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Verb(Base):
    __tablename__ = 'verbs'

    id = Column(Integer, primary_key=True, index=True)
    verb = Column(String(50), nullable=False)
    examples = relationship("Example", back_populates="verb")

class Example(Base):
    __tablename__ = 'examples'

    id = Column(Integer, primary_key=True, index=True)
    verb_id = Column(Integer, ForeignKey('verbs.id'))
    english = Column(String(255), nullable=False)
    korean = Column(String(255), nullable=False)
    verb = relationship("Verb", back_populates="examples")

Base.metadata.create_all(bind=engine)