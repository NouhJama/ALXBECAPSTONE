from rest_framework.pagination import CursorPagination

# class PortfolioCursorPagination(CursorPagination):
#     page_size = 10
#     ordering = 'id'  # Order by created_at descending

class TransactionCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-transaction_date'  # Order by transaction_date descending

class AssetCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'  # Order by updated_at descending