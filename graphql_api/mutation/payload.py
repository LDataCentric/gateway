import graphene
from controller.auth import manager as auth
from graphql_api import types
from controller.auth.manager import get_user_by_info
from controller.payload import manager
from graphql_api.types import InformationSourcePayload


class CreatePayload(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID()
        information_source_id = graphene.ID()
        asynchronous = graphene.Boolean(required=False)

    payload = graphene.Field(InformationSourcePayload)

    def mutate(self, info, project_id: str, information_source_id: str, asynchronous: bool = True):
        auth.check_demo_access(info)
        auth.check_project_access(info, project_id)
        user = get_user_by_info(info)
        payload = manager.create_payload(
            info, project_id, information_source_id, user.id, asynchronous
        )
        return CreatePayload(payload)


class TrainAllModels(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID()

    payload = graphene.List(InformationSourcePayload)

    def mutate(self, info, project_id: str, asynchronous: bool = False):
        auth.check_demo_access(info)
        auth.check_project_access(info, project_id)
        user = get_user_by_info(info)
        payload = manager.train_all_models(
            info, project_id, user.id, asynchronous
        )
        return TrainAllModels(payload)


class PayloadMutation(graphene.ObjectType):
    create_payload = CreatePayload.Field()
    train_all_models = TrainAllModels.Field()
