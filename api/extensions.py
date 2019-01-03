import graphene
from graphene_django.converter import convert_django_field


class ExampleQuery:
    class Meta:
        object_type = "api.schema.ExampleType"
        single_name = "example"
        plural_name = "examples"
        identifiers = (("id",),)


def create_query_set_accessor(cls, query_set):
    if query_set is not None:
        return lambda self: query_set
    return lambda self: getattr(self, cls.Meta.list_name)


def build_model_query(cls, query_set=None):
    get_query_set = create_query_set_accessor(cls, query_set)
    return type("ModelQuery", (), {
        cls.Meta.single_name: graphene.Field(cls.Meta.object_type, **cls.Meta.unique_arguments),
        cls.Meta.plural_name: graphene.List()
    })
