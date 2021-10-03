from os import system
from typing import List, Optional

from sqlmodel import Field, Session, SQLModel, create_engine, or_, select, Relationship


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates='team')


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

    team_id: Optional[int] = Field(default=None, foreign_key='team.id')
    team: Optional[Team] = Relationship(back_populates='heroes')


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(
            name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)

        hero_black_lion = Hero(
            name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("Team Wakaland:", team_wakaland)

        hero_tarantula = Hero(
            name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(
            name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)
        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)


def select_heroes():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        result = session.exec(statement)
        team_preventers = result.one()

        print("Preventers heroes:", team_preventers.heroes)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        result = session.exec(statement)
        hero_spider_boy = result.one()

        hero_spider_boy.team = None
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_spider_boy)
        print("Spider-Boy without team:", hero_spider_boy)

# def select_heroes():
#     with Session(engine) as session:
#         hero_spider_boy = session.exec(
#             select(Hero).where(Hero.name == "Spider-Boy")).one()

#         print("hero_spider_boy: ", hero_spider_boy.name,
#               "team: ", hero_spider_boy.team)

# def create_heroes():
#     with Session(engine) as session:
#         team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
#         team_z_force = Team(
#             name="Z-Force", headquarters="Sister Margaret’s Bar")
#         session.add(team_preventers)
#         session.add(team_z_force)
#         session.commit()

#         hero_deadpond = Hero(
#             name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
#         )
#         hero_rusty_man = Hero(
#             name="Rusty-Man",
#             secret_name="Tommy Sharp",
#             age=48,
#             team_id=team_preventers.id,
#         )
#         hero_spider_boy = Hero(
#             name="Spider-Boy", secret_name="Pedro Parqueador")
#         session.add(hero_deadpond)
#         session.add(hero_rusty_man)
#         session.add(hero_spider_boy)
#         session.commit()

#         session.refresh(hero_deadpond)
#         session.refresh(hero_rusty_man)
#         session.refresh(hero_spider_boy)

#         print("Created hero:", hero_deadpond)
#         print("Created hero:", hero_rusty_man)
#         print("Created hero:", hero_spider_boy)

#         hero_spider_boy.team_id = team_preventers.id
#         session.add(hero_spider_boy)
#         session.commit()
#         session.refresh(hero_spider_boy)
#         print("Updated hero:", hero_spider_boy)

#         hero_spider_boy.team_id = None
#         session.add(hero_spider_boy)
#         session.commit()
#         session.refresh(hero_spider_boy)
#         print("No longer Preventer:", hero_spider_boy)

#         print('______________')


# def select_heroes():
#     with Session(engine) as session:
#         results = session.exec(
#             select(Hero, Team).join(Team, isouter=True).where(Team.name == "Preventers"))
#         for hero, team in results:
#             print("Hero:", hero, "Team:", team)


# def select_heroes():
#     with Session(engine) as session:
#         results = session.exec(
#             select(Hero, Team).where(Hero.team_id == Team.id))


#         for hero, team in results:
#             print("Hero:", hero, "Team:", team)


# def create_heroes():
#     hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
#     hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
#     hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
#     hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
#     hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
#     hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
#     hero_7 = Hero(name="Captain North America",
#                   secret_name="Esteban Rogelios", age=93)

#     with Session(engine) as session:
#         session.add(hero_1)
#         session.add(hero_2)
#         session.add(hero_3)
#         session.add(hero_4)
#         session.add(hero_5)
#         session.add(hero_6)
#         session.add(hero_7)

#         session.commit()


# def select_heroes():
#     with Session(engine) as session:
#         results = session.exec(select(Hero).offset(3).limit(3)).all()
#         print(10*'-')
#         print(results)
#         print(10*'-')


# def select_hero():
#     with Session(engine) as session:
#         result = session.exec(select(Hero).where(Hero.name != "Deadpond").where(
#             or_(Hero.age <= 35, Hero.age > 90)))
#         for hero in result:
#             print(hero)


# def update_heroes():
#     with Session(engine) as session:
#         statement = select(Hero).where(Hero.name == "Spider-Boy")
#         results = session.exec(statement)
#         hero = results.one()  # one: if results != 1: raise error!
#         print("Hero:", hero)

#         hero.age = 10
#         session.add(hero)
#         session.commit()
#         session.refresh(hero)
#         print("Hero:", hero)


# def delete_heroes():
#     with Session(engine) as session:
#         statement = select(Hero).where(Hero.name == "Spider-Boy")
#         results = session.exec(statement)
#         hero = results.one()
#         print("Hero: ", hero)

#         session.delete(hero)
#         session.commit()


def main():
    system("rm database.db")
    create_db_and_tables()
    create_heroes()
    select_heroes()
    # select_hero()
    update_heroes()
    # delete_heroes()


if __name__ == "__main__":
    main()
