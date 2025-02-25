from typing import Union
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine, select
import os



DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:saetfo2025@database:5432/postgres")

# Crear la conexión con PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# Modelo de Usuario con SQLModel
class User(SQLModel, table=True):
    id: int | None = None
    name: str

# Crear tablas en la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Dependencia para obtener la sesión
def get_session():
    with Session(engine) as session:
        yield session

# Endpoint para agregar un usuario
@app.post("/users/")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Endpoint para obtener todos los usuarios
@app.get("/users/")
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.get("/")
def read_root():
    return {"message": "¡FastAPI con SQLModel y PostgreSQL en Docker funcionando!"}