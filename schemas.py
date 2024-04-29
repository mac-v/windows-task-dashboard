## serializaiton = python -> JSON (dump_only)
## deserialization JSON -> python (load_only)
from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str()
    report_name = fields.Str()
    author = fields.Str()
    schedule_type = fields.Str()
    time_trigger_interval = fields.Str()
    calendar_trigger_days= fields.Str()
    execution_time =fields.DateTime()

# Defining fields and their behaviour at output and input
class PlainItemSchema(Schema):
    # dump only means that it can be used for returning data from API
    # it is not for sending
    # we receive it JSON payload
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemUpdateSchema(Schema):
    # dump only means that it can be used for returning data from API
    # it is not for sending
    # we receive it JSON payload
    name = fields.Str()
    price = fields.Float()
    store_id=fields.Int()
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
