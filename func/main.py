# Jormungandr
from src.domain.enums import CodeResponse
from src.domain.exceptions import InvalidJwtToken
from src.domain.response.model import ResponseModel
from src.services.jwt import JwtService
from src.services.post_user_ticket import CreateTicketService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
import flask

from src.services.snapshot import SnapshotUserDataService


def post_user_ticket():
    message = "Jormungandr::post_user_account_close"
    jwt = flask.request.headers.get("x-thebes-answer")
    try:
        JwtService.apply_authentication_rules(jwt=jwt)
        decoded_jwt = JwtService.decode_jwt(jwt=jwt)
        # snapshot = SnapshotUserDataService.get_snapshot(jwt=jwt)
        success = CreateTicketService.set_tickets(
            snapshot="Cliente deseja encerramento de conta",
            decoded_jwt=decoded_jwt,
        )

        response_model = ResponseModel.build_response(
            success=success,
            code=CodeResponse.SUCCESS,
            message="Ticket posted successfully",
        )

        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.CREATED
        )
        return response

    except InvalidJwtToken as ex:
        Gladsheim.error(error=ex, message=f"{message}::Invalid JWT token")
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.JWT_INVALID,
            message=ex.msg,
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.UNAUTHORIZED
        )
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=f"{message}::{str(ex)}")
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return response
