
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select, func, text


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    secret_name: str
    age: Optional[int] = None


mysql_url = "mysql+pymysql://root:123456@localhost:9999/djangodemo?charset=utf8mb4"

engine = create_engine(mysql_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():  #
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")  #
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:  #
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        print("After adding to the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        session.commit()

        print("After committing the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        print("After committing the session, show IDs")
        print("Hero 1 ID:", hero_1.id)
        print("Hero 2 ID:", hero_2.id)
        print("Hero 3 ID:", hero_3.id)

        print("After committing the session, show names")
        print("Hero 1 name:", hero_1.name)
        print("Hero 2 name:", hero_2.name)
        print("Hero 3 name:", hero_3.name)

def main():  #
    # create_db_and_tables()  #
    # create_heroes()  #
    with Session(engine) as session:  #

        stmt = select(func.count(Hero.age).label(
            "age_count"), Hero.age.label("h")).where(Hero.age != None).group_by(Hero.age).having(text("age_count > 5"))
        results = session.exec(stmt)
        print(results.all())
        print(stmt)

        #


if __name__ == "__main__":  #
    main()  #
