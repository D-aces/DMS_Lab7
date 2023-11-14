from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bus_routes/", views.bus_routes, name="bus_routes"),
    path("bus_route_detail/", views.bus_route_detail, name="bus_route_detail"),

    # REST Framework URLS
    path('api/get_defined_bus_trip/', include('transitapp.api.urls', 'transitapp_api'))
]