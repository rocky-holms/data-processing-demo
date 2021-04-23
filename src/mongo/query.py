import os

from mongoengine import connect, disconnect
from src.mongo.models import Record
from yaml import dump

connect(os.environ.get("MONGO_DB_NAME"), host=os.environ.get("MONGO_DB_HOST"))


def get_all_records_db():
    records = [
        record.to_mongo().to_dict() for record in Record.objects.all().exclude("id")
    ]
    data = dump(records)
    disconnect()
    return data


def get_by_customer_by_type(customer_type):
    records = [
        record.to_mongo().to_dict()
        for record in Record.objects(customer_type__iexact=customer_type).exclude("id")
    ]
    data = dump(records)
    disconnect()
    return data


def get_by_customer_by_travel_type(travel_type):
    records = [
        record.to_mongo().to_dict()
        for record in Record.objects(type_of_travel__iexact=travel_type).exclude("id")
    ]
    data = dump(records)
    disconnect()
    return data


def get_by_customer_by_class(class_type):
    records = [
        record.to_mongo().to_dict()
        for record in Record.objects(flight_class__iexact=class_type).exclude("id")
    ]
    data = dump(records)
    disconnect()
    return data
