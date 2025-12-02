from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[str] = mapped_column(
        String(60), unique=True, nullable=False)

    favorites: Mapped["Favorites"] = relationship(back_populates="user")
    people: Mapped["People"] = relationship(back_populates="user")
    vehicles: Mapped["Vehicles"] = relationship(back_populates="user")
    planets: Mapped["Planets"] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="people")
    favorites: Mapped["Favorites"] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height
        }


class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    length: Mapped[int] = mapped_column(nullable=True)
    passengers: Mapped[int] = mapped_column(nullable=True)
    cargo_capacity: Mapped[int] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="vehicles")
    favorites: Mapped["Favorites"] = relationship(back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "length": self.length,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=True)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    gravity: Mapped[int] = mapped_column(nullable=True)
    terrain: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[int] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="planets")
    favorites: Mapped["Favorites"] = relationship(back_populates="planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "population": self.population
        }


class Favorites(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), nullable=True)
    vehicles_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), nullable=True)
    planets_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")
    vehicles: Mapped["Vehicles"] = relationship(back_populates="favorites")
    planets: Mapped["Planets"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "vehicles_id": self.vehicles_id,
            "planets_id": self.planets_id
        }
