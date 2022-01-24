from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='Home Page'),
    path('room/new/', views.AddNewRoom.as_view(), name="New Conference Room"),
    path('rooms', views.ShowRooms.as_view(), name="Show all rooms"),
    path('room/delete/<int:room_to_del>', views.DeleteRoom.as_view(), name="Delete room"),
    path('room/modify/<int:room_to_mod>', views.ModifyRoom.as_view(), name="Modify room"),
]
