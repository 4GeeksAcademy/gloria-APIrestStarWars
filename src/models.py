from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            # No serializar la contraseña por seguridad
        }
    def serialize_favorites(self):
        return [favorite.serialize() for favorite in self.favorites] if len(self.favorites) > 0 else []


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(80), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="character")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gravity: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    poblation: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="planets")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "climate": self.climate,
            "poblation": self.poblation,
            "rotation_period": self.rotation_period
        }


class Films(db.Model):
    __tablename__ = "films"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created: Mapped[str] = mapped_column(String(80), nullable=False)
    edited: Mapped[str] = mapped_column(String(100), nullable=False)
    producer: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="films")

    def __repr__(self):
        return '<Films %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created,
            "edited": self.edited,
            "producer": self.producer,
            "title": self.title,
            "director": self.director
        }


class Favorites(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    planets_id: Mapped[int | None] = mapped_column(ForeignKey("planets.id"), nullable=True)
    character_id: Mapped[int | None] = mapped_column(ForeignKey("character.id"), nullable=True)
    films_id: Mapped[int | None] = mapped_column(ForeignKey("films.id"), nullable=True)

    user: Mapped["User"] = relationship("User")
    planets: Mapped["Planets"] = relationship("Planets")
    character: Mapped["Character"] = relationship("Character")
    films: Mapped["Films"] = relationship("Films")

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "character": self.character.serialize() if self.character else None,
            "planet": self.planets.serialize() if self.planets else None,
            "film": self.films.serialize() if self.films else None,
        }