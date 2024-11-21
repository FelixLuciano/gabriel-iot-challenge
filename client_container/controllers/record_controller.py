import datetime

from flask_restx import Api

from connections import DatabaseConnection, CameraConnection
from errors import NotFoundError
from models import RecordModel, RecordTypeModel, DiscEventModel


class RecordController:
    def __init__(self, context: Api):
        self.context = context
        self.database_connection = DatabaseConnection(context)
        self.camera_connection = CameraConnection(context)

    def get_by_date(self, reference_date: datetime.date):
        with self.database_connection.get_session() as session:
            records = RecordModel.get_by_date(session, reference_date)

            if len(records) > 0:
                return list(map(RecordModel.to_dto, records))

        try:
            record_data = self.camera_connection.fetch_day(reference_date.year, reference_date.month, reference_date.day)
        except NotFoundError:
            return []
        
        records = self._decode_record_data(record_data)

        with self.database_connection.get_session() as session:
            session.add_all(records)
            session.commit()

        return list(map(RecordModel.to_dto, records))

    def get_by_period(self, reference_start: datetime.datetime, reference_end: datetime.datetime):
        with self.database_connection.get_session() as session:
            records = RecordModel.get_by_period(session, reference_start, reference_end)

            if len(records) > 0:
                return list(map(RecordModel.to_dto, records))

        records = []
        reference_delta = reference_end - reference_start

        for day in range(reference_delta.days + 2):
            reference_date = reference_start + datetime.timedelta(days=day)

            try:
                record_data = self.camera_connection.fetch_day(reference_date.year, reference_date.month, reference_date.day)
                day_records = self._decode_record_data(record_data)

                records.extend(day_records)
            except NotFoundError:
                return []

        with self.database_connection.get_session() as session:
            session.add_all(records)
            session.commit()

        return list(map(RecordModel.to_dto, records))

    def get_by_day(self, year: int, month: int, day: int):
        with self.database_connection.get_session() as session:
            records = RecordModel.get_by_day(session, year, month, day)

            if len(records) > 0:
                return list(map(RecordModel.to_dto, records))

        try:
            record_data = self.camera_connection.fetch_day(year, month, day)
        except NotFoundError:
            return []
        
        records = self._decode_record_data(record_data)

        with self.database_connection.get_session() as session:
            session.add_all(records)
            session.commit()

        return list(map(RecordModel.to_dto, records))

    def get_by_month(self, year: int, month: int):
        with self.database_connection.get_session() as session:
            records = RecordModel.get_by_month(session, year, month)

            if len(records) > 0:
                return list(map(RecordModel.to_dto, records))

        try:
            record_data = self.camera_connection.fetch_month(year, month)
        except NotFoundError:
            return []

        records = []

        for day, has_rec in enumerate(record_data["is_has_rec"], 1):
            if has_rec != 1:
                continue

            try:
                record_data = self.camera_connection.fetch_day(year, month, day)
                day_records = self._decode_record_data(record_data)

                records.extend(day_records)
            except NotFoundError:
                continue

        with self.database_connection.get_session() as session:
            session.add_all(records)
            session.commit()

        return list(map(RecordModel.to_dto, records))

    def get_by_year(self, year: int):
        with self.database_connection.get_session() as session:
            records = RecordModel.get_by_year(session, year)

            if len(records) > 0:
                return list(map(RecordModel.to_dto, records))

        records = []

        for month in range(1, 13):
            try:
                month_records =self.get_by_month(year, month)

                records.extend(month_records)
            except NotFoundError:
                continue

        return records

    def _decode_record_data(self, record_data):
        records = []

        with self.database_connection.get_session() as session:
            for event in record_data["record"][0]:
                record = self._decode_camera_event(session, event)

                records.append(record)

        return records

    @staticmethod
    def _decode_camera_event(session, event: dict):
        datetime_format = "%m/%d/%Y %H:%M:%S"

        start_datetime_str = " ".join([event["start_date"], event["start_time"]])
        end_datetime_str = " ".join([event["end_date"], event["end_time"]])
        start_datetime = datetime.datetime.strptime(start_datetime_str, datetime_format)
        end_datetime = datetime.datetime.strptime(end_datetime_str, datetime_format)
        record_type = RecordTypeModel.get_by_id(session, event["record_type"])
        disc_event = DiscEventModel.get_by_id(session, event["disk_event_id"])

        return RecordModel.create(
            internal_record_id=event["record_id"],
            start_time=start_datetime,
            end_time=end_datetime,
            record_size=event["size"],
            record_type=record_type,
            disc_event=disc_event,
        )
