import graphene
from graphql.error import GraphQLError
from graphene_django.types import DjangoObjectType
from django.utils.functional import SimpleLazyObject

from . import models


class AuthenticationError(GraphQLError):
    """Raised when a session token is invalid."""


def detail_query(query_set=None):
    """A strange workaround for templating the detail query.

    We need this in order to be able to either look into self.details
    or models.Details.objects based on the specific query scope.
    """

    class DetailQuery:
        detail = graphene.Field("api.query.DetailType", name=graphene.String(), value=graphene.String())
        details = graphene.List("api.query.DetailType")

        def resolve_detail(self, info, **kwargs):
            name = kwargs.get("name")
            value = kwargs.get("value")
            if name is not None and value is not None:
                return query_set(self).filter(name=name, value=value).first()
            return None

        def resolve_details(self, info, **kwargs):
            return query_set(self).all()

    return DetailQuery


class InputCategory(graphene.InputObjectType):
    name = graphene.String()


def item_query(query_set):
    """Same thing as above. There should be a better way to do this."""

    class ItemQuery:
        item = graphene.Field("api.query.ItemType", id=graphene.Int())
        items = graphene.List("api.query.ItemType")

        def resolve_item(self, info, **kwargs):
            id = kwargs.get("id")
            if id is not None:
                return query_set(self).filter(users=info.context.user, id=id).get()
            return None

        def resolve_items(self, info, **kwargs):
            return query_set(self).filter(users=info.context.user).all()

    return ItemQuery


class SessionType(
        detail_query(lambda self: models.Detail.objects),
        item_query(lambda self: models.Item.objects),
        DjangoObjectType):
    """The session type is my way around the need for stateless
    authentication. All queries must be routed through the session,
    which is only available by filtration based on the login token.
    The models provided through this session are then filtered by the
    corresponding user to the token."""

    class Meta:
        model = models.Session

    location = graphene.Field("api.query.LocationType", id=graphene.Int())
    locations = graphene.List("api.query.LocationType")

    def resolve_location(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.Location.objects.filter(user=info.context.user).get(id=id)
        return None

    def resolve_locations(self, info, **kwargs):
        return models.Location.objects.filter(user=info.context.user).all()

    category = graphene.Field("api.query.CategoryType", name=graphene.String())
    categories = graphene.List("api.query.CategoryType")

    def resolve_category(self, info, **kwargs):
        name = kwargs.get("name")
        if name is not None:
            return models.Category.objects.filter(user=info.context.user).get(name=name)
        return None

    def resolve_categories(self, info, **kwargs):
        return models.Category.objects.filter(user=info.context.user).all()

    list = graphene.Field("api.query.ListType", id=graphene.Int(), name=graphene.String())
    lists = graphene.List("api.query.ListType")

    def resolve_list(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.List.objects.filter(user=info.context.user).get(id=id)
        return None

    def resolve_lists(self, info, **kwargs):
        return models.List.objects.filter(user=info.context.user).all()

    transaction = graphene.Field("api.query.TransactionType", id=graphene.Int())
    transactions = graphene.List("api.query.TransactionType")

    def resolve_transaction(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.Transaction.objects.filter(user=info.context.user).get(id=id)
        return None

    def resolve_transactions(self, info, **kwargs):
        return models.Transaction.objects.filter(user=info.context.user).all()

    movement = graphene.Field("api.query.MovementType", id=graphene.Int())
    movements = graphene.List("api.query.MovementType")

    def resolve_movement(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return models.Transaction.objects.filter(user=info.context.user).get(id=id)
        return None

    def resolve_movements(self, info, **kwargs):
        return models.Transaction.objects.filter(user=info.context.user).all()


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        only_fields = ("username", "first_name", "last_name", "email")


SelfDetailQuery = detail_query(lambda self: self.details)
SelfItemQuery = item_query(lambda self: self.items)


class LocationType(SelfItemQuery, DjangoObjectType):
    class Meta:
        model = models.Location


class CategoryType(SelfItemQuery, DjangoObjectType):
    class Meta:
        model = models.Category


class DetailType(SelfItemQuery, DjangoObjectType):
    class Meta:
        model = models.Detail


class ListType(SelfItemQuery, DjangoObjectType):
    class Meta:
        model = models.List


class ItemType(SelfDetailQuery, DjangoObjectType):
    class Meta:
        model = models.Item


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction


class MovementType(DjangoObjectType):
    class Meta:
        model = models.Movement


class Query(graphene.ObjectType):
    session = graphene.Field("api.query.SessionType", token=graphene.String())

    def resolve_session(self, info, **kwargs):
        token = kwargs.get("token")
        if token is not None:
            session = models.Session.objects.filter(token=token).first()
            if session is not None:
                info.context.user = SimpleLazyObject(lambda: session.user)
                return session
        raise AuthenticationError("No valid session!")
