from sqlalchemy.orm import Mapped, mapped_column, Session

from models.base_model import BaseModel


class DiscEventModel(BaseModel):
    __tablename__ = "DiscEvent"

    enumerator: Mapped[str] = mapped_column(unique=True, nullable=False)

    @staticmethod
    def create(id: int, enumerator: str):
        disc_event = DiscEventModel()

        disc_event.id = id
        disc_event.enumerator = enumerator

        return disc_event

    @staticmethod
    def get_by_id(session, id: int):
        return (
            session.query(DiscEventModel)
            .where(DiscEventModel.id == id)
            .one()
        )

    @staticmethod
    def get_by_enumerator(session: Session, enumerator: str):
        return (
            session.query(DiscEventModel)
            .where(DiscEventModel.enumerator == enumerator)
            .one()
        )
