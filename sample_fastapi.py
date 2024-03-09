from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True, index=True)
    password = Column(String)

app = FastAPI()

engine = create_engine('sqlite:///./test.db')
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username):
    with SessionLocal() as session:
        return session.query(User).filter(User.username == username).first()

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"message": "Login successful!"}

@app.get("/login_form", response_class=HTMLResponse)
async def login_form():
    return """
    <form method="post">
    <label>Username: <input type="text" name="username"></label><br>
    <label>Password: <input type="password" name="password"></label><br>
    <button type="submit">Login</button>
    </form>
    """
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)