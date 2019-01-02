import graphene

from . import models


class User:
    user = graphene.Field("api.schema.UserType", username=graphene.String())
    users = graphene.List("api.schema.UserType")

    # Resolvers
    def resolve_user(self, info, **kwargs):
        username = kwargs.get("username")
        if username is not None:
            return (self and self.users or models.User.objects).get(username=username)
        return None

    def resolve_users(self, info, **kwargs):
        return (self and self.users or models.User.objects).all()


class Location:
    location = graphene.Field("api.schema.LocationType", id=graphene.Int())
    locations = graphene.List("api.schema.LocationType")

    def resolve_location(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return (self and self.locations or models.Location.objects).get(id=id)
        return None

    def resolve_locations(self, info, **kwargs):
        return (self and self.locations or models.Location.objects).all()


class Category:
    category = graphene.Field("api.schema.CategoryType", name=graphene.String())
    categories = graphene.List("api.schema.CategoryType")

    def resolve_category(self, info, **kwargs):
        name = kwargs.get("name")
        if name is not None:
            return (self and self.categories or models.Category.objects).get(name=name)
        return None

    def resolve_categories(self, info, **kwargs):
        return (self and self.categories or models.Category.objects).all()


class Detail:
    detail = graphene.Field("api.schema.DetailType", name=graphene.String(), value=graphene.String())
    details = graphene.List("api.schema.DetailType")

    def resolve_detail(self: models.Item, info, **kwargs):
        query = {}  # We want to be able to query one or the other or both
        name = kwargs.get("name")
        value = kwargs.get("value")
        if name is not None:
            query["name"] = name
        if value is not None:
            query["value"] = value
        if name is not None or value is not None:
            return (self and self.details or models.Detail.objects).filter(**query).first()
        return None

    def resolve_details(self, info, **kwargs):
        return (self and self.details or models.Detail.objects).all()


class List:
    list = graphene.Field("api.schema.ListType", id=graphene.Int(), name=graphene.String())
    lists = graphene.List("api.schema.ListType")

    def resolve_list(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return (self and self.lists or models.List.objects).get(id=id)
        return None

    def resolve_lists(self, info, **kwargs):
        return (self and self.lists or models.List.objects).all()


class Item:
    item = graphene.Field("api.schema.ItemType", id=graphene.Int())
    items = graphene.List("api.schema.ItemType")

    def resolve_item(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return (self and self.items or models.Item.objects).get(id=id)
        return None

    def resolve_items(self, info, **kwargs):
        return (self and self.items or models.Item.objects).all()
