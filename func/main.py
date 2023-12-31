# Jormungandr
# Standards
from http import HTTPStatus

import flask
# Third party
from etria_logger import Gladsheim

from src.domain.enums.enums import CodeResponse
from src.domain.exceptions.exceptions import InvalidJwtToken, JormungandrCommunication, ErrorWithZendesk, \
    UnableToBuildSnapshot
from src.domain.models.response.model import ResponseModel
from src.services.jwt.service import JwtService
from src.services.snapshot.service import SnapshotUserDataService
from src.services.zendesk.service import CreateTicketService


def post_user_ticket():
    message = "Jormungandr::post_user_ticket"
    jwt = flask.request.headers.get("x-thebes-answer")
    try:
        JwtService.apply_authentication_rules(jwt=jwt)
        decoded_jwt = JwtService.decode_jwt(jwt=jwt)
        snapshot = SnapshotUserDataService.get_snapshot(jwt=jwt)
        success = CreateTicketService.set_tickets(
            decoded_jwt=decoded_jwt,
            snapshot=snapshot,
            jwt=jwt,
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

    except ValueError as ex:
        Gladsheim.error(ex=ex, message=f'{message}::There are invalid format or extra parameters')
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.INVALID_PARAMS,
            message="There are invalid format or extra/missing parameters",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.BAD_REQUEST
        )
        return response

    except (JormungandrCommunication, ErrorWithZendesk, UnableToBuildSnapshot) as ex:
        Gladsheim.error(ex=ex, message=f'{message}::{ex.msg}')
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.PARTNERS_ERROR_ON_API_REQUEST,
            message=ex.msg,
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.SERVICE_UNAVAILABLE
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
