from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from .filters import UserFilter
from .models import User
from .serializers import UserSerializer


@extend_schema_view(
    list=extend_schema(summary="List users", description="Paginated; supports filtering, search and ordering."),
    create=extend_schema(summary="Create a user", description="Requires a JWT access token."),
    retrieve=extend_schema(summary="Get a user"),
    update=extend_schema(summary="Replace a user", description="Requires a JWT access token."),
    partial_update=extend_schema(summary="Partially update a user", description="Requires a JWT access token."),
    destroy=extend_schema(summary="Delete a user", description="Requires a JWT access token."),
)
@extend_schema(tags=["users"])
class UserViewSet(viewsets.ModelViewSet):
    """CRUD for users: list, create, retrieve, update, partial_update, destroy."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UserFilter
    search_fields = ["name"]
    ordering_fields = ["id", "name", "age"]
