from django.shortcuts import render

# DRF imports
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# django-filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
import django_filters

# Imports Categories
from .models import Category
from .serializers import CategorySerializer

# Imports Listings
from .models import Listing, ListingImage
from .serializers import (
    ListingSerializer,
    ListingCreateSerializer,
    ListingImageSerializer,
    ListingListSerializer,
    ListingDetailSerializer
)
from .permissions import IsOwnerOrReadOnly


# ---------- FILTERSET (najważniejsza część!) ----------
class ListingFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category__id")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Listing
        fields = ["category", "min_price", "max_price"]


# ---------- LIST + CREATE ----------
class ListingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Listing.objects.all().order_by("-created_at")
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ListingCreateSerializer
        return ListingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


# ---------- RETRIEVE / UPDATE / DELETE ----------
class ListingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ListingCreateSerializer
        return ListingSerializer

    def perform_update(self, serializer):
        serializer.save()


# ---------- MULTI IMAGE UPLOAD ----------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_images(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    files = request.FILES.getlist("images")
    created = []
    start_order = listing.images.count()

    for idx, f in enumerate(files):
        img = ListingImage.objects.create(listing=listing, image=f, order=start_order + idx)
        created.append(ListingImageSerializer(img, context={"request": request}).data)

    return Response({"uploaded": created}, status=status.HTTP_201_CREATED)


# ---------- CATEGORY LIST ----------
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    # pagination_class = None


# ---------- LISTING LIST (CORE) ----------
class ListingListAPIView(generics.ListAPIView):
    queryset = Listing.objects.all().order_by("-created_at")
    serializer_class = ListingListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    pagination_class = PageNumberPagination
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

    # Najważniejsze:
    filterset_class = ListingFilter

    search_fields = ["title", "description"]


# ---------- LISTING DETAIL ----------
class ListingDetailAPIView(generics.RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingDetailSerializer
    lookup_field = "id"
