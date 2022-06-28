# Third part
from etria_logger import Gladsheim
from zenpy.lib.api_objects import User, Ticket, Via, Comment

# Jormungandr
from ...domain.enums import TicketType
from ...infrastructure.zendesk.infrastructure import ZendeskInfrastructure


class ZendeskRepository:
    infra = ZendeskInfrastructure
    method = Via(source="api")
    SUBJECT = "Encerramento de Conta"
    TICKET_TYPE = TicketType.PROBLEM.value

    @classmethod
    def get_user(cls, unique_id: str) -> User:
        zenpy_client = cls.infra.get_connection()
        if user_results := zenpy_client.users(external_id=unique_id):
            user_zenpy = user_results.values[0]
            return user_zenpy

    @classmethod
    def create_user(cls, user_data: dict) -> User:
        user_obj = User(
            name=user_data["nick_name"],
            email=user_data["email"],
            external_id=user_data["unique_id"]
        )
        zenpy_client = cls.infra.get_connection()
        try:
            user = zenpy_client.users.create(user_obj)
            return user
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Jormungandr::CreateTicketService::create_user::Failed to create user",
            )
            raise ex

    @staticmethod
    def set_comment(user: User, snapshot: str) -> Comment:
        comment = Comment(
            author_id=user.id,
            html_body=snapshot,
            public=False,
        )
        return comment

    @classmethod
    def set_ticket(cls, user: User, comment: Comment) -> Ticket:
        ticket = Ticket(
            subject=cls.SUBJECT,
            requester_id=user.id,
            ticket_type=cls.TICKET_TYPE,
            via=ZendeskRepository.method,
            comment=comment,
        )
        return ticket

    @classmethod
    def post_ticket(cls, ticket: Ticket) -> bool:
        zenpy_client = cls.infra.get_connection()
        try:
            zenpy_client.tickets.create(ticket)
            return True
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Jormungandr::CreateTicketService::set_tickets::Failed to create ticket",
            )
            raise ex
