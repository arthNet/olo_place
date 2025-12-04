from django.urls import path
from .views import ListingListCreateAPIView, ListingRetrieveUpdateDestroyAPIView, upload_images, CategoryListAPIView, ListingListAPIView, ListingDetailAPIView



urlpatterns = [
    path("listings/", ListingListCreateAPIView.as_view(), name="listings-list-create"),
    path("listings/<int:pk>/", ListingRetrieveUpdateDestroyAPIView.as_view(), name="listings-detail"),
    path("listings/<int:pk>/upload_images/", upload_images, name="listing-upload-images"),
    path("listings-simple/", ListingListAPIView.as_view(), name="listings"),
    path("categories/", CategoryListAPIView.as_view(), name="categories-list"),
    path("", ListingListAPIView.as_view(), name="listing-list"),
    path("<int:id>/", ListingDetailAPIView.as_view(), name="listing-detail"),
]
