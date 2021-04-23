import logging
import os
import traceback
from csv import DictReader
from io import StringIO

from mongoengine import connect, disconnect
from src.utils.parse_record import create_record

from celery import states

from .worker import celery_conn

connect(os.environ.get("MONGO_DB_NAME"), host=os.environ.get("MONGO_DB_HOST"))


@celery_conn.task(name="process_data.task", bind=True)
def process_data(self, file):
    try:
        csv_data = file.decode("utf-8")
        reader = DictReader(StringIO(csv_data))

        records = list(reader)
        records_processed = 0

        number_of_records = len(records)

        for row in records:
            record = create_record(row)

            if record:
                try:
                    record.save()
                except Exception as e:
                    logging.error(e)

            records_processed += 1
            self.update_state(
                state="PROGRESS",
                meta={"done": records_processed, "total": number_of_records},
            )

        disconnect()
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": type(ex).__name__,
                "exc_message": traceback.format_exc().split("\n"),
            },
        )
        raise ex
