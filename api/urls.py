from django.urls import path
# from .views import DumpItAPI
from . import views
urlpatterns = [
    path('', views.getMe),
    path('add/', views.postMe),
    path('michael/', views.getMichaelStats),
    path('geo/', views.getGeoStats),
    path('delete/<int:game_id>/', views.deleteGameByID)
 
 
    # path('add/', DumpItAPI.as_view()),
    # path('update/<int:id>/', DumpItAPI.as_view()),
    # path('delete/', DumpItAPI.as_view())
]