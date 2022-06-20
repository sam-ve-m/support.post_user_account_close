# Jormungandr
from func.src.domain.enums import CodeResponse
from func.src.domain.exceptions import InvalidJwtToken
from func.src.domain.response.model import ResponseModel
from func.src.services.jwt import JwtService
from func.src.services.post_user_ticket import CreateTicketOfAccountCloseService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request


def post_user_ticket():
    message = "Jormungandr::post_user_ticket"
    jwt = request.headers.get("x-thebes-answer")
    try:
        JwtService.apply_authentication_rules(jwt=jwt)
        decoded_jwt = JwtService.decode_jwt(jwt=jwt)
        client_ticket_service = CreateTicketOfAccountCloseService(
            jwt=jwt,
            decoded_jwt=decoded_jwt,
        )
        success = client_ticket_service.set_tickets()

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
