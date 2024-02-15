import random
import uuid

import factory

from app.models import Staff, Document


class DefaultFactory(factory.alchemy.SQLAlchemyModelFactory):
    ...


class StaffFactory(DefaultFactory):
    """Factory class for Staff objects."""

    class Meta:
        model = Staff

    uid = factory.Sequence(lambda _: uuid.uuid4())
    internal_id = factory.Sequence(lambda _: uuid.uuid4())


class DocumentFactory(DefaultFactory):
    """Factory class for Document objects"""

    class Meta:
        model = Document

    uid = factory.Sequence(lambda _: uuid.uuid4())
    total = factory.Sequence(lambda _: random.choice(range(10, 100)))
