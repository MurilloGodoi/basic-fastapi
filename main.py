from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import model
from database import SessionLocal, engine
import schema

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://petbam.com.br",
        "https://*.petbam.com.br",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)       


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/produtos", response_model=schema.Product)
def list_products(product: schema.ProductCreate, db: Session = Depends(get_db)):
    db_product = model.Product(
        name=product.name,
        category=product.category,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/produtos", response_model=List[schema.Product])
def list_products(db: Session = Depends(get_db)):
    return db.query(model.Product).all()


@app.get("/produtos/{id}", response_model=schema.Product)
def get_product(id: int, db: Session = Depends(get_db)):
    return db.query(model.Product).filter_by(id=id).first()


@app.put("/produtos/{id}", response_model=schema.Product)
def update_product(id: int, product: schema.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(model.Product).filter_by(id=id).first()

    db_product.name = product.name
    db_product.category = product.category
    db_product.price = product.price

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product
