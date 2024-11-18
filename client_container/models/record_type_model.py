from sqlalchemy.orm import Mapped, mapped_column, Session

from models.base_model import BaseModel


class RecordTypeModel(BaseModel):
    __tablename__ = "RecordType"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    enumerator: Mapped[str] = mapped_column(unique=True, nullable=False)

    @staticmethod
    def create(id: int, enumerator: str):
        disc_event = RecordTypeModel()

        disc_event.id = id
        disc_event.enumerator = enumerator

        return disc_event

    @staticmethod
    def get_by_id(session, id: int):
        return (
            session.query(RecordTypeModel)
            .where(RecordTypeModel.id == id)
            .one()
        )

    @staticmethod
    def get_by_enumerator(session: Session, enumerator: str):
        return (
            session.query(RecordTypeModel)
            .where(RecordTypeModel.enumerator == enumerator)
            .one()
        )