# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel
# import bcrypt

# # 데이터베이스 URL 설정
# DATABASE_URL = "postgresql://wonde:981023@localhost/testbase"

# # SQLAlchemy 설정
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # SQLAlchemy 모델 정의 (테이블 정의)
# class Dish(Base):
#     __tablename__ = "dishes"  # 테이블 이름

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     price = Column(Integer)

# class User(Base):
#     __tablename__ = "users"  # 유저 테이블 정의

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

# # 데이터베이스 테이블 생성
# Base.metadata.create_all(bind=engine)

# # FastAPI 앱 생성
# app = FastAPI()

# # Pydantic 모델 (API 요청 데이터 검증용)
# class DishCreate(BaseModel):
#     name: str
#     price: int

# class UserCreate(BaseModel):
#     username: str
#     password: str

# # 데이터베이스 세션 함수
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Helper function to hash the password
# def hash_password(plain_password: str) -> str:
#     return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# # POST: 새로운 항목 추가
# @app.post("/cart/")
# def add_cart(dish: DishCreate, db: Session = Depends(get_db)):
#     db_dish = Dish(name=dish.name, price=dish.price)
#     db.add(db_dish)
#     db.commit()
#     db.refresh(db_dish)
#     return db_dish

# # GET: 모든 항목 조회
# @app.get("/cart/")
# def see_cart(db: Session = Depends(get_db)):
#     return db.query(Dish).all()

# # PUT: 항목 수정
# @app.put("/cart/{dish_id}")
# def edit_dish(dish_id: int, edited_dish: DishCreate, db: Session = Depends(get_db)):
#     dish = db.query(Dish).filter(Dish.id == dish_id).first()
#     if dish is None:
#         raise HTTPException(status_code=404, detail="Dish not found")
    
#     dish.name = edited_dish.name
#     dish.price = edited_dish.price
#     db.commit()
#     return dish

# # DELETE: 항목 삭제
# @app.delete("/cart/{dish_id}")
# def delete_dish(dish_id: int, db: Session = Depends(get_db)):
#     dish = db.query(Dish).filter(Dish.id == dish_id).first()
#     if dish is None:
#         raise HTTPException(status_code=404, detail="Dish not found")
    
#     db.delete(dish)
#     db.commit()
#     return {"message": "Dish deleted"}

# # Route for user sign-up
# @app.post("/signup")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = hash_password(user.password)
    
#     # Check if the username already exists
#     existing_user = db.query(User).filter(User.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
    
#     # Create a new user instance and add it to the database
#     db_user = User(username=user.username, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)  # Refresh to get the updated user with its id

#     return {"message": "User created successfully"}

# from fastapi.security import OAuth2PasswordBearer
# from fastapi import status

# # Pydantic model for user login
# class UserLogin(BaseModel):
#     username: str
#     password: str

# # OAuth2 token generator (required if you decide to use token-based authentication like JWT)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Helper function to verify the password
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# # Route for user login
# @app.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     # Fetch the user's hashed password from the database based on the username
#     db_user = db.query(User).filter(User.username == user.username).first()

#     if db_user is None:
#         raise HTTPException(status_code=400, detail="Invalid username or password")

#     # Verify the entered password with the stored hashed password
#     if not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid username or password")

#     # If successful, return a success message (you can return a token here in the future)
#     return {"message": "Login successful"}


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import bcrypt

DATABASE_URL = "postgresql://wonde:981023@localhost/testbase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name =  Column(String, index=True)
    price = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class DishCreate(BaseModel):
    name: str
    price: int

class UserCreate(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@app.post("/cart/")
def add_cart(dish: DishCreate, db: Session = Depends(get_db)):
    db_dish = Dish(name=dish.name, price=dish.price)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

@app.get("/cart/")
def see_cart(keyword: str = None, db: Session = Depends(get_db)):
    if keyword:
        dishes = db.query(Dish).filter(Dish.name.ilike(f"%{keyword}%").all_)
    else:
        dishes = db.query(Dish).all()
    return dishes

@app.put("/cart/{dish_id}")
def edit_dish(dish_id: int, edited_dish: DishCreate, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
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
    
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}

class UserLogin(BaseModel):
    username: str
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"message": "Login successful"}
