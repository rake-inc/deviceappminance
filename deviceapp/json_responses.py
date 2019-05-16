from rest_framework.status import (
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_201_CREATED,
    HTTP_202_ACCEPTED, HTTP_417_EXPECTATION_FAILED, is_success,
    is_client_error)


class ResponseCode(object):
    message = {
        HTTP_405_METHOD_NOT_ALLOWED: "Method not allowed",
        HTTP_400_BAD_REQUEST: "Bad request",
        HTTP_404_NOT_FOUND: "Not found",
        HTTP_403_FORBIDDEN: "Forbidden",
        HTTP_401_UNAUTHORIZED: "Unauthorized request",
        HTTP_200_OK: "Ok",
        HTTP_201_CREATED: "Successfully created",
        HTTP_202_ACCEPTED: "Accepted",
        HTTP_417_EXPECTATION_FAILED: "Expectation failed",
    }

    @classmethod
    def response_message(cls, status):
        if is_success(status):
            return {"success": True, "message": cls.message.get(status, "OK")}
        elif is_client_error(status):
            return {
                "success": False,
                "message": cls.message.get(status, "Broken request")
            }
        return {
            "success": False,
            "message": cls.message.get(status, "Something went wrong")
        }


def response_message_from_status(status_code=200):
    if isinstance(status_code, int):
        return ResponseCode.response_message(status_code)
    else:
        return status_code
