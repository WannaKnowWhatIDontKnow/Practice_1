'''First, you have to install things on the terminal.
What were those?'''
'''
pip install FastApi #this one for API
pip install uvicorn #this one for web server
pip install pydantic #this one for data validation
pip install sqlalchemy #this one for... session?
pip install bcrypt #this one for hashing passwords
pip install psycopg2  #this one for... not sure 
'''  

'''Import the libraries
that help you build things'''
from fastapi import FastAPI, Depends, HTTPException
'''FastAPI helps create... a web, and Depends helps...
improve the stability of codes?... and HTTPException
apparently helps deal with errors... but not sure'''
from sqlalchemy import create_engine, Column, Integer, String
'''engine is the pipeline that connects between a db
and a web. And coloumn, integer, string... not sure
why needed.'''
from sqlalchemy.ext.declarative import declarative_base
'''I still don't get why i would need that 
ext thing and declarative thing...'''
from sqlalchemy.orm import sessionmaker, Session 
'''Session is sth that helps me connect to the db
through the engine.'''
from pydantic import BaseModel
import bcrypt
''' pydantic helps validate incoming data to the db,
and bcrypt allows to hash passwords.'''

DATABASE_URL = "postgresql://wonde:981023@localhost/testbase"
#what it does? why needed? 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, \
                            autoflush=False, \
                                bind=engine)
#autocommit false? what's that flush thing? bind? 
Base = declarative_base() #what is that?... to validate?

class Dish(Base):
    __tablename__ = "dishes"
#those four underbars are... mandatory?
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
#so... it creates a column for each and defines types.

class User(Base):
    __tablename__ =  "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    '''what matters here is that i must make sure whether
    a certain cell could go without a value, and whether 
    the value is generic or unique.'''
    hashed_password = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)
#what's metadata? what's bind?

app = FastAPI()

class DishCreate(BaseModel):
    name: str
    price: int
#what's the difference between Base and BaseModel? 
#and between Dish and DishCreate?

class UserCreate(BaseModel):
    username: str
    password: str

def get_db():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''what exactly does it do? sth about session creation...
but doesn't make sense to me quite well. what're those
try, yield, finally? Why would you need them?'''

def hash_password(plain_password: str) -> str: #this means... this value can be transformed into str...?
    return bcrypt.hashpw(plain_password.encode('utf-8'), \
                         bcrypt.gensalt()).decode('utf-8')
#wth? encode... decode... utf-8... gensalt... what are those?


@app.post("/cart/") #what if I remove that second slash?
def add_cart(dish: DishCreate, db: Session = Depends(get_db)): #stil...  doesn't feel intuitive
    db_dish =  Dish(name=dish.name, price=dish.price) #why not just 'dish', but have to create 'db_dish'?
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

@app.get("/cart/")
def see_cart(keyword: str = None, db: Session = Depends(get_db)):
    if keyword:
        dishes = db.query(Dish).filter(Dish.name.ilike(f"%{keyword}%")).all()
    else:
        dishes = db.query(Dish).all()
    return dishes

@app.put("/cart/{dish_id}")
def edit_dish(dish_id: int, edited_dish: DishCreate, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found") #what if this line's gone?
    dish.name = edited_dish.name
    dish.price = edited_dish.price
    db.commit()
    return dish

@app.delete("/cart/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    db.delete(dish)
    db.commit()
    return {"message": "Dish deleted"}

@app.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = User(username = user.username, hashed_password = hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    #what if I don't hash passwords?
    return {"message": "User created successfully"}

class UserLogin(BaseModel):
    username: str
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #why boolean? Could you just compare by using = or sth?
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')) #not decode, but two encodes?
@app.post("/login") #why just a single slash? 
def login(user: UserLogin, db: Session = Depends(get_db)): #what's the difference between : and = in ()?
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalide username or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        #difference between "if ~ is none / if not ~"?
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"message": "Login successful"}
