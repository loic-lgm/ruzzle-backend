from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.category.models import Category
from apps.brand.models import Brand
from apps.user.serializers import UserSerializer
from apps.category.serializers import CategorySerializer
from apps.brand.serializers import BrandSerializer


class SearchView(APIView):
    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if not q:
            return Response({"users": [], "categories": [], "brands": []})

        User = get_user_model()

        users = User.objects.filter(username__istartswith=q, is_active=True).exclude(
            is_staff=True, is_superuser=True
        )[:5]
        categories = Category.objects.filter(name__icontains=q)[:5]
        brands = Brand.objects.filter(name__icontains=q)[:5]

        return Response(
            {
                "users": UserSerializer(users, many=True).data,
                "categories": CategorySerializer(categories, many=True).data,
                "brands": BrandSerializer(brands, many=True).data,
            }
        )
