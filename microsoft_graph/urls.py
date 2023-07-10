from django.urls import path
from microsoft_graph.views import GetGraphAuthUrl, GraphRedirectUri

urlpatterns = [
    path('get_graph_auth_api/', GetGraphAuthUrl.as_view()),
    path("graph_redirect_uri", GraphRedirectUri.as_view())
]