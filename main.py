
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select, func, text, and_, col, Column, TIMESTAMP, DateTime
from typing import Optional
from pydantic import BaseModel
# from sqlalchemy import Column, TIMESTAMP
from datetime import datetime
app = FastAPI()


class Book():
    def __init__(self, id, title, author, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.published_year = published_year


mysql_url = "mysql+pymysql://root:123456@localhost:9999/djangodemo?charset=utf8mb4"

engine = create_engine(mysql_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_session():
    with Session(engine) as session:
        yield session
        print(123)


class User(BaseModel):
    name: str
    password: str
    birthday: datetime

    class Config:

        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }


# class Hero(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: Optional[int] = None

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    secret_name: str
    age: Optional[int] = None
#  方式一 有用
    create_at: Optional[datetime] = Field(
        sa_column=Column(DateTime,
                         nullable=False, server_default=func.now())
    )

    update_at: Optional[datetime] = Field(
        sa_column=Column(DateTime,
                         nullable=False,
                         server_default=func.now(), onupdate=func.now())
    )

#  下面方式二 没用
    # create_at: Optional[datetime] = Field(sa_column=Column(
    #     TIMESTAMP(timezone=True),
    #     nullable=False,
    #     server_default=text("CURRENT_TIMESTAMP"),
    # ))
    # update_at: Optional[datetime] = Field(sa_column=Column(
    #     TIMESTAMP(timezone=True),
    #     nullable=False,
    #     server_default=text("CURRENT_TIMESTAMP"),
    #     server_onupdate=text("CURRENT_TIMESTAMP"),
    # ))


class User(BaseModel):
    name: str
    password: str
    birthday: datetime

    class Config:

        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }


class HeroResponse(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }


@app.get("/method")
def method():
    return Book(1, "Harry Potter", "J.K. Rowling", 1997)


@app.get("/user/me")
def user_me():
    return User(name="John", password="secret", birthday="2022-12-12 23:01:23")


@app.post("/hero")
def create_hero(seesion: Session = Depends(get_session)):
    hero1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=12)
    hero2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=40)
    seesion.add(hero1)
    seesion.add(hero2)
    seesion.commit()
    return {
        "code": 200,
        "msg": "success"
    }


@app.put("/hero")
def update_hero(name: str, seesion: Session = Depends(get_session)):
    hero = seesion.get(Hero, 1)
    hero.name = name
    seesion.add(hero)
    seesion.commit()
    seesion.refresh(hero)
    return hero

def say(data):
    print(data)

@app.get("/herofilter", response_model=list[HeroResponse])
def filter_hero(seesion: Session = Depends(get_session)):
    # stmt = select(func.count(Hero.age).label("ageCount"), Hero.age.label("heroAge")).where(
    #     Hero.age != None).group_by(Hero.age).having(text("ageCount > 1"))

    # stmt = select(func.count(Hero.age).label("ageCount"), Hero.age.label(
    #     "heroAge")).group_by(Hero.age).group_by(Hero.name).having(
    #     and_(func.count(Hero.age) > 0, Hero.age != None))

    # stmt = select(func.count(Hero.age).label("ageCount"), Hero.age.label(
    #     "heroAge"), Hero.name).group_by(Hero.age).group_by(Hero.name)

    # stmt = select(func.count(Hero.age).label("ageCount"), Hero.age.label(
    #     "heroAge"), text("group_concat(name) as name")).group_by(Hero.age)

    # stmt = select(func.count(Hero.age).label("ageCount"), Hero.age.label(
    #     "heroAge"), func.group_concat(Hero.name).label("names")).group_by(Hero.age)

    # stmt = text('''
    #         SELECT count(hero.age) AS "ageCount", hero.age AS "heroAge", group_concat(name) as name
    #             FROM hero GROUP BY hero.age;
    #             '''
    #             )

    #     stmt = """
    #     select * from hero;
    # """

    stmt = select(Hero)
    print(stmt)
    ret = seesion.exec(stmt).all()
    say(ret)
    print(ret)
    return ret
