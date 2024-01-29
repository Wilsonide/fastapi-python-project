from fastapi import FastAPI
from . import models
from .database import engine
from .settings import setting
from .routers import post, user, auth, votes


models.Base.metadata.create_all(bind=engine)

""" while True:
    try:
        conn = psycopg2.connect(
        host = getenv("DB_HOST"),
        database = getenv("DB_NAME"),
        user = getenv("DB_USER "),
        password = getenv("DB_PASSWORD"),cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as e:
        print("Error creating database")
        print(e)
        sleep(5) """


app = FastAPI()
print(setting.ACCESS_TOKEN_EXPIRE_MINUTES)
print(setting.ALGORITHM)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get('/')
def root():
    return {"message": "welcome to the post"}
