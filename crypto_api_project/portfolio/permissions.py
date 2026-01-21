from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming the model instance has an `owner` attribute.
        return obj.owner == request.user
    
class IsAssetOwner(BasePermission):
    """
    Custom permission to only allow owners of the asset to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming the Asset model instance has a `portfolio` attribute with an `owner`.
        return obj.portfolio.owner == request.user
    
class IsTransactionOwner(BasePermission):
    """
    Custom permission to only allow owners of the transaction to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming the Transaction model instance has an `asset` attribute
        # which in turn has a `portfolio` attribute with an `owner`.
        return obj.asset.portfolio.owner == request.user