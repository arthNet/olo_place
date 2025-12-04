from rest_framework import serializers
from .models import Listing, ListingImage, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent")

class ListingImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ListingImage
        fields = ("id", "url", "order")

    def get_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return None

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ("id", "title", "description", "price", "category", "owner", "images", "created_at", "updated_at")

class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ("title", "description", "price", "category")
extra_kwargs = {
    "category": {"required": False, "allow_null": True}
}

# Serializer for listing summaries
class ListingListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "category",
            "owner",
            "created_at",
        ]

# Serializer for listing detail view
class ListingDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "category",
            "owner",
            "created_at",
            "updated_at",
        ]
