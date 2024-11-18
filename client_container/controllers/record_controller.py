from datetime import datetime

from flask import Flask

from connections import DatabaseConnection, CameraConnection
from errors import NotFoundError
from models import RecordModel, DiscEventModel


class RecordController:
    def __init__(self, context: Flask):
        self.context = context
        self.database_connection = DatabaseConnection(context)
        self.camera_connection = CameraConnection(context)

    def get_by_month(self, month: int):
        # with self.database_connection.get_session() as session:
        #     record = RecordModel.get_by_month(session, month)

        #     if record is not None:
        #         return record
    
        month_records = self.camera_connection.fetch_month(month)

        records = []

        with self.database_connection.get_session() as session:
            for day, has_rec in enumerate(month_records["is_has_rec"], 1):
                if has_rec != 1:
                    continue

                try:
                    record_data = self.camera_connection.fetch_day(day, month)
                except NotFoundError:
                    continue

                datetime_format = "%m/%d/%Y %H:%M:%S"

                for event in record_data["record"][0]:
                    start_datetime_str = " ".join([event["start_date"], event["start_time"]])
                    end_datetime_str = " ".join([event["end_date"], event["end_time"]])
                    start_datetime = datetime.strptime(start_datetime_str, datetime_format)
                    end_datetime = datetime.strptime(end_datetime_str, datetime_format)
                    disc_event = DiscEventModel.get_by_id(session, event["disk_event_id"])

                    record = RecordModel.create(
                        internal_record_id=event["record_id"],
                        start_time=start_datetime,
                        end_time=end_datetime,
                        record_size=event["size"],
                        disc_event=disc_event,
                    )

                    records.append(record)

            session.add_all(records)
            session.commit()

        self.context.logger.debug(records)

        return list(map(lambda a: a.record_size, records))
