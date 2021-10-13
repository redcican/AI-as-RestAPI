import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class SMSInference(Model):
    __keyspace__ = 'spam_inference'
    uuid = columns.UUID(primary_key=True, default=uuid.uuid1)
    query = columns.Text()
    label = columns.Text()
    confidence = columns.Float()
    model_version = columns.Text(default="v1")