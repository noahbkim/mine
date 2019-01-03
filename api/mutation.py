import graphene
from django.contrib.auth import authenticate


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    token = graphene.String()

    def mutate(self, info, username, password):
        authenticate(info.context, username=username, password=password)
        return Login(token=info.context.token)


class Mutation(graphene.ObjectType):
    login = Login.Field()
