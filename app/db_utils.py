"""
Utility functions used for database operations
"""
import sys

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import flag_modified

from app import db
# from app.models import Stories


def create_object(obj):
    """
    A utility function to add an object to the database
    :param obj: the object that is being added to the database
    :return: no return value, an object will be added to the database
    """
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Failed to CREATE {} : {}".format(obj, e))
        print(sys.exc_info())
    # else:
    #     # create elasticsearch doc
    #     if (not isinstance(obj, Storie)
    #         and hasattr(obj, 'es_create')
    #         and current_app.config['ELASTICSEARCH_ENABLED']):
    #           obj.es_create()
    #     return str(obj)


def update_object(data, obj_type, obj_id, es_update=True, by_email=False):
    """
    Update a database record and its elasticsearch counterpart.
    :param data: a dictionary of attribute-value pairs
    :param obj_type: sqlalchemy model
    :param obj_id: id of record
    :param es_update: update the elasticsearch index
    :param by_email: boolean indicating whether identifier is an email
    :return: was the record updated successfully?
    """
    if by_email:
        obj = get_object_by_email(obj_type, obj_id)
    else:
        obj = get_object(obj_type, obj_id)

    if obj:
        for attr, value in data.items():
            if isinstance(value, dict):
                # update json values
                attr_json = getattr(obj, attr) or {}
                for key, val in value.items():
                    attr_json[key] = val
                setattr(obj, attr, attr_json)
                flag_modified(obj, attr)
            else:
                setattr(obj, attr, value)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception("Failed to UPDATE {}".format(obj))
        else:
            # update elasticsearch
            if hasattr(obj, 'es_update') and current_app.config['ELASTICSEARCH_ENABLED'] and es_update:
                obj.es_update()
            return True
    return False


def get_object(obj_type, obj_id):
    """
    Safely retrieve a database record by its id
    and its sqlalchemy object type.
    """
    if not obj_id:
        return None
    try:
        return obj_type.query.get(obj_id)
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception('Error searching "{}" table for id {}'.format(
            obj_type.__tablename__, obj_id))
        return None

def get_object_by_email(model, email):
    """
    Retrieve an object from the database by its email.
    :param model: The SQLAlchemy model class representing the database table
    :param email: The unique identifier for the object
    :return: The object if found, None otherwise
    """
    try:
        return model.query.filter_by(email=email).first()
    except SQLAlchemyError as e:
        current_app.logger.exception("Database error occurred while retrieving object by email: {}".format(e))
        return None
