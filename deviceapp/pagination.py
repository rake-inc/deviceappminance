from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .json_responses import response_message_from_status


class Pagination(object):
    def __init__(self, request, items, meta, page_size=20):
        self.items = items
        self.meta = meta
        self.page_size = int(request.GET.get('page_size', page_size))
        self.page_no = request.GET.get('page', 1)
        self.url = request.path
        self.response = {}
        self.paginator = None
        self.status_code = 200
        self.obj_list = []

    def get_next_link(self):
        try:
            if self.paginator.page(self.page_no).has_next():
                return self.url + '?page=' + str(
                    self.paginator.page(self.page_no).next_page_number()) + '&page_size=' + str(self.page_size)
        except EmptyPage:
            pass
        except PageNotAnInteger:
            pass
        return None

    def get_previous_link(self):
        try:
            if self.paginator.page(self.page_no).has_previous():
                return self.url + '?page=' + str(
                    self.paginator.page(self.page_no).previous_page_number()) + '&page_size=' + str(self.page_size)
        except EmptyPage:
            pass
        except PageNotAnInteger:
            pass
        return None

    @property
    def start_index(self):
        return self.paginator.page(self.page_no).start_index()

    @property
    def end_index(self):
        return self.paginator.page(self.page_no).end_index()

    def prepare_response(self):

        self.meta = {
            "page_no": self.page_no,
            "type": "list",
            "total_items": self.paginator.count,
            "total_pages": self.paginator.num_pages,
            "next_page": self.get_next_link(),
            "previous_page": self.get_previous_link(),
            # "start_index": self.start_index,
            # "end_index": self.end_index,
            "per_page": self.paginator.per_page
        }

        self.response = {"items": self.obj_list, "meta": self.meta}

    def paginate(self):
        self.paginator = Paginator(self.items, per_page=self.page_size)
        try:
            cur_page = self.paginator.page(self.page_no)
            self.obj_list = cur_page.object_list
            page_range = self.paginator.page_range
            self.prepare_response()

        except EmptyPage:
            self.page_no = 1
            cur_page = self.paginator.page(self.page_no)

        except (PageNotAnInteger, ValueError):
            self.status_code = 400
            self.response = response_message_from_status(self.status_code)

    def paginated_response(self):
        self.paginate()
        return self.response
