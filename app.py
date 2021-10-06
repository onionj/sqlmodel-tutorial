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


def main():
    system("rm database.db")
    create_db_and_tables()


if __name__ == "__main__":
    main()
