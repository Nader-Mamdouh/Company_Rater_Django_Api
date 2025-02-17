from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from .serializers import StockCompanySerializer, StockRatingSerializer, UserSerializer
from .models import StockCompany, StockRating
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authtoken.models import Token


class StockCompanyViewSet(viewsets.ModelViewSet):
    queryset = StockCompany.objects.all()
    serializer_class = StockCompanySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def rate_stock(self, request, pk=None):
        if 'rating' in request.data:  # Use correct key
            stock = get_object_or_404(StockCompany, id=pk)
            stars = request.data['rating']
            if not (1 <= int(stars) <= 5):
                return Response({"message": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = request.user
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                rating = StockRating.objects.get(user=user, company=stock)
                rating.rating = stars  # Update the rating
                rating.save()
                message = "Rating updated"
            except StockRating.DoesNotExist:
                rating = StockRating.objects.create(
                    user=user, company=stock, rating=stars)
                message = "Rating created"

            return Response({"message": message, "rating": rating.rating}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class StockRatingViewSet(viewsets.ModelViewSet):
    queryset = StockRating.objects.all()
    serializer_class = StockRatingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = {
            "message": "Wrong Way to create"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {
            "message": "Wrong Way to update"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        if company_id:
            return StockRating.objects.filter(company__id=company_id)
        return StockRating.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            'token': token.key,
        },
            status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
