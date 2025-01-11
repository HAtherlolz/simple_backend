"""
Override the PageNumberPagination for pagination
"""
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """
    Class Pagination to paginate query
    page_size (int): a param default number of units per page
    page_size_query_param (str): a param to set a name of query param
        of number page_size
    page_query_param (int): a param to set a name of query param
        of number of page

    """
    page_size = 10
    page_size_query_param = 'per_page'
    page_query_param = 'page'
