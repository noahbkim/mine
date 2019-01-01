import graphene
from graphene_django.types import DjangoObjectType

from . import models
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # fields = ("id", "username", "first_name", "last_name")

    # TODO: limit field access


class LocationType(DjangoObjectType):
    class Meta:
        model = models.Location


class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Category


class DetailType(DjangoObjectType):
    class Meta:
        model = models.Detail


class PackingListType(DjangoObjectType):
    class Meta:
        model = models.PackingList


class ItemType(DjangoObjectType):
    class Meta:
        model = models.Item


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction


class Query(graphene.ObjectType):

    # List queries
    users = graphene.List(LocationType)
    locations = graphene.List(LocationType)
    categories = graphene.List(CategoryType)
    details = graphene.List(DetailType)
    packing_lists = graphene.List(PackingListType)
    items = graphene.List(ItemType)
    transactions = graphene.List(TransactionType)

    # Resolvers
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_locations(self, info, **kwargs):
        return models.Location.objects.all()

    def resolve_categories(self, info, **kwargs):
        return models.Category.objects.all()

    def resolve_details(self, info, **kwargs):
        return models.Detail.objects.all()

    def resolve_packing_lists(self, info, **kwargs):
        return models.PackingList.objects.all()

    def resolve_items(self, info, **kwargs):
        return models.Item.objects.all()

    def resolve_transactions(self, info, **kwargs):
        return models.Transaction.objects.all()

    # Single items
    user = graphene.Field(UserType, username=graphene.String())
    location = graphene.Field(LocationType, name=graphene.String())
    category = graphene.Field(CategoryType, name=graphene.String())
    packing_list = graphene.Field(PackingListType, id=graphene.Int(), name=graphene.String())
    item = graphene.Field(ItemType, id=graphene.Int())
    transaction = graphene.Field(TransactionType, id=graphene.Int())

    # Resolvers
    def resolve_user(self, info, **kwargs):
        username = kwargs.get("username")
        if username is not None:
            return User.objects.get(username=username)
        return None

    def resolve_location(self, info, **kwargs):
        name = kwargs.get("name")
        if name is not None:
            return models.Location.objects.get(name=name)
        return None

    def resolve_category(self, info, **kwargs):
        name = kwargs.get("name")
        if name is not None:
            return models.Category.objects.get(name=name)
        return None

    def resolve_packing_list(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.PackingList.objects.get(id=id)
        return None

    def resolve_item(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.Item.objects.get(id=id)
        return None

    def resolve_transaction(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.Transaction.objects.get(id=id)
        return None


schema = graphene.Schema(query=Query)
