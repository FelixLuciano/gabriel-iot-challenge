from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey

from models.base_model import BaseModel
from models.disc_event_model import DiscEventModel
from models.record_type_model import RecordTypeModel


class RecordModel(BaseModel):
    __tablename__ = "Record"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    internal_record_id: Mapped[int] = mapped_column(nullable=False)
    record_type_id: Mapped[int] = mapped_column(ForeignKey("RecordType.id"), nullable=False)
    disk_event_id: Mapped[int] = mapped_column(ForeignKey("DiscEvent.id"), nullable=False)
    record_size: Mapped[int] = mapped_column(nullable=False)

    record_type: Mapped[RecordTypeModel] = relationship(lazy="selectin")
    disk_event: Mapped[DiscEventModel] = relationship(lazy="selectin")

    def __dict__(self):
        return {
            "test": 123,
        }

    @staticmethod
    def create(
        internal_record_id: int,
        start_time: datetime,
        end_time: datetime,
        disc_event: DiscEventModel,
        record_size: int,
    ):
        record = RecordModel()

        record.internal_record_id = internal_record_id
        record.start_time = start_time
        record.end_time = end_time
        record.disk_event = disc_event
        record.record_size = record_size

        return record

    @staticmethod
    def get_by_month(session: Session, reference_month: int):
        return (
            session.query(RecordModel)
            .where(RecordModel.reference_month == reference_month)
            .first()
        )
