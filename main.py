from fastapi import FastAPI, Depends, Form, Request
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import Boolean, Column, Integer, String
from datetime import date
from fastapi.responses import HTMLResponse, RedirectResponse    
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    dob: date
    # phone: int
    address: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def save_kyc_data(db: Session, kyc_data: UserBase):
    db_user = models.User(
        firstname=kyc_data.firstname,
        lastname=kyc_data.lastname,
        email=kyc_data.email,
        dob=kyc_data.dob,
        address=kyc_data.address
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/submit_kyc/")
async def submit_kyc(firstname: str = Form(...),
                     lastname: str = Form(...),
                     address: str = Form(...),
                     dob: date=Form(...),
                     email: str=Form(...),
                    #  phone: int= Form(...),
                     db: Session = Depends(get_db)):
    kyc_data = UserBase(firstname=firstname, email=email, lastname=lastname,dob=dob, address=address)
    db_user = save_kyc_data(db, kyc_data)
    return RedirectResponse(url="/", status_code=303)
