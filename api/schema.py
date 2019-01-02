import graphene
from graphql.error import GraphQLError
from graphene_django.types import DjangoObjectType

from . import models
from . import query


class UnauthorisedAccessError(GraphQLError):
    """Raised to prevent access to sensitive parts of existing models/"""

    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class UserType(query.Location, query.Category, query.Item, query.List, DjangoObjectType):
    class Meta:
        model = models.User
        only_fields = ("username", "first_name", "last_name", "email")


class LocationType(query.Item, DjangoObjectType):
    class Meta:
        model = models.Location


class CategoryType(query.Item, DjangoObjectType):
    class Meta:
        model = models.Category


class DetailType(query.Item, DjangoObjectType):
    class Meta:
        model = models.Detail


class ListType(ItemQuery, DjangoObjectType):
    class Meta:
        model = models.List


class ItemType(UserQuery, DetailQuery, DjangoObjectType):
    class Meta:
        model = models.Item


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction


class Query(UserQuery, DetailQuery, graphene.ObjectType):

    # Transaction
    transaction = graphene.Field("api.schema.TransactionType", id=graphene.Int())
    transactions = graphene.List("api.schema.TransactionType")

    def resolve_transaction(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.Transaction.objects.get(id=id)
        return None

    def resolve_transactions(self, info, **kwargs):
        return models.Transaction.objects.all()


schema = graphene.Schema(query=Query)
