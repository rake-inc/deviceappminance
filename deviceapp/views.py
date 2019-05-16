from rest_framework import status
from rest_framework.response import Response
from .json_responses import response_message_from_status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .pagination import Pagination
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .json_responses import response_message_from_status
from drf_ujson.renderers import UJSONRenderer as JsonRenderer
import collections
import ujson


class BaseView(APIView):
    response_context = {"meta": {}, "items": []}

    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.args = ()
        self.kwargs = {}
        self.request = None
        self.headers = {}

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        REST API calls will be dispatched here.
        :request Request object
        :args None
        :kwargs Provided in the URL patterns and slug fields in the URL
        :returns Dispatches response to the client
        """
        if kwargs.get('type', False) == 'detail':
            setattr(request, 'paginate', False)
        else:
            setattr(request, 'paginate', True)
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        defined_methods = set(self.http_method_names).intersection(
            set(dir(self)))

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in defined_methods:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                # handler = self.http_method_not_allowed
                return self.dispatch_response(
                    status.HTTP_405_METHOD_NOT_ALLOWED)

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        return self.dispatch_response(response)

    def dispatch_response(self, response, meta=response_context['meta']):
        """
        Finalizes the type of response based on the response content and
        paginates if required and prepares meta information and then the
         response will be dispatched.
        :response response content or response object or serializer instance
        or status code or raw data of type (str,list,tuple)
        :meta dict from the member variable by default
        :return Finalized response object (<Response object>)
        """

        formatted_response = Response(self.response_context)

        if type(response) is not int:
            if self.request.method in ["POST", "PATCH"]:
                response.content_type = self.request.META.get("CONTENT_TYPE", "text/html")
            elif self.request.method in ["GET", "PUT"]:
                response.content_type = self.request.META.get("HTTP_ACCEPT", "application/json")

        if hasattr(response, 'data'):
                items = response.data
                if hasattr(response, 'status_code'):
                    formatted_response = self.formatted_response(items, status_code=response.status_code)
                else:
                    formatted_response = self.formatted_response(items)

        elif isinstance(response, int):
            status_code = response
            meta.update(response_message_from_status(status_code))
            formatted_response = Response(
                self.response_context, status=status_code)

        elif isinstance(response, Response):
            formatted_response = response

        return self.finalize_response(self.request, formatted_response)

    def formatted_response(self,
                           items,
                           meta=response_context['meta'],
                           status_code=200):
        """
        Formats the response with pagination and meta information and
        returns an Response object.
        :items serialized data of type dict or OrderedDict.
        :status_code status code
        :return <Response object>
        """

        if self.request.paginate and not isinstance(items, dict):
            pagination = Pagination(self.request, items, meta)
            response_dict = self.convert_to_dict(
                pagination.paginated_response())
            return Response(response_dict, status=pagination.status_code)

        else:
            meta.update({"type": "detail"})
            self.response_context = self.convert_to_dict({
                "items":
                    items if not isinstance(items, list) else items[0],
                "meta":
                    meta,
            })

        return Response(self.response_context, status=status_code)

    @staticmethod
    def convert_to_dict(data):
        return ujson.loads(ujson.dumps(data))
