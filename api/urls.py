from django.urls import path
from .views import UserListView, ExampleView

urlpatterns = [
	path('ExampleView', ExampleView.as_view(), name='ExampleView'),
	path('', UserListView.as_view(), name='api-userlist'),

]
