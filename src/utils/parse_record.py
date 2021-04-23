import logging

from src.api.models import Record
from src.mongo.models import Record as MongoRecord


def record_check(row):
    try:
        if row.get(""):
            del row[""]
        record = Record(**row)
        return record.dict(exclude_none=True)
    except Exception as e:
        logging.error(f"Unable to parse record {row}")
        logging.error(e)
        return False


def create_record(row):
    row_parsed = record_check(row)

    if row_parsed:
        try:
            record = MongoRecord(**row_parsed)
            return record
        except Exception as e:
            logging.error(f"Unable to save record to database {row_parsed}")
            logging.error(e)
