import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey, extract

from models.base_model import BaseModel
from models.disc_event_model import DiscEventModel
from models.record_type_model import RecordTypeModel


class RecordModel(BaseModel):
    __tablename__ = "Record"

    start_time: Mapped[datetime.datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(nullable=False)
    internal_record_id: Mapped[int] = mapped_column(nullable=False)
    record_type_id: Mapped[int] = mapped_column(ForeignKey("RecordType.id"), nullable=False)
    disk_event_id: Mapped[int] = mapped_column(ForeignKey("DiscEvent.id"), nullable=False)
    record_size: Mapped[int] = mapped_column(nullable=False)

    record_type: Mapped[RecordTypeModel] = relationship(lazy="selectin")
    disk_event: Mapped[DiscEventModel] = relationship(lazy="selectin")

    def to_dto(self):
        return {
            "record_id": self.internal_record_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "size": self.record_size,
            "record_type": self.record_type.enumerator,
            "disk_event": self.disk_event.enumerator,
        }

    @staticmethod
    def create(
        internal_record_id: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        record_type: RecordTypeModel,
        disc_event: DiscEventModel,
        record_size: int,
    ):
        record = RecordModel()

        record.internal_record_id = internal_record_id
        record.start_time = start_time
        record.end_time = end_time
        record.record_type = record_type
        record.disk_event = disc_event
        record.record_size = record_size

        return record

    @staticmethod
    def get_by_date(session: Session, reference_date: datetime.date):
        return (
            session.query(RecordModel)
            .where(
                RecordModel.start_time >= reference_date,
                RecordModel.end_time <= reference_date,
            )
            .all()
        )

    @staticmethod
    def get_by_period(session: Session, reference_start: datetime.datetime, reference_end: datetime.datetime):
        return (
            session.query(RecordModel)
            .where(
                RecordModel.start_time >= reference_start,
                RecordModel.end_time <= reference_end,
            )
            .all()
        )

    @staticmethod
    def get_by_day(session: Session, year: int, month: int, day: int):
        return (
            session.query(RecordModel)
            .where(
                extract("year", RecordModel.start_time) >= year,
                extract("year", RecordModel.end_time) <= year,
                extract("month", RecordModel.start_time) >= month,
                extract("month", RecordModel.end_time) <= month,
                extract("day", RecordModel.start_time) >= day,
                extract("day", RecordModel.end_time) <= day,
            )
            .all()
        )

    @staticmethod
    def get_by_month(session: Session, year: int, month: int):
        return (
            session.query(RecordModel)
            .where(
                extract("month", RecordModel.start_time) >= month,
                extract("month", RecordModel.end_time) <= month,
            )
            .all()
        )

    @staticmethod
    def get_by_year(session: Session, year: int):
        return (
            session.query(RecordModel)
            .where(
                extract("year", RecordModel.start_time) >= year,
                extract("year", RecordModel.end_time) <= year,
            )
            .all()
        )
