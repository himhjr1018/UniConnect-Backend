from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests
from datetime import datetime, timedelta
from microsoft_graph import config
from users.models import UserProfile


# Create your views here.


class GetGraphAuthUrl(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        graph_auth_api = f"https://login.microsoftonline.com/common/oauth2/" +\
            f"v2.0/authorize?client_id={config.clientId}&"\
                f"response_type=code&redirect_uri={config.redirectUri}&response_mode=form_post&scope=offline_access"+\
                        f"%20contacts.read%20user.read&state={request.user.id}"
        return Response({"OauthUrl": graph_auth_api}, status=status.HTTP_200_OK)


class GraphRedirectUri(APIView):
    def post(self, request):
        graph_token_api = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        post_data = {
            "client_id": config.clientId,
            "scope": config.graphUserScopes,
            "grant_type": "authorization_code",
            "client_secret": config.clientSecret,
            "redirect_uri": config.accessRedirectUri,
            "code": request.data["code"],
        }
        resp = requests.post(graph_token_api, data=post_data).json()
        print(resp)
        profile = UserProfile.objects.get(id=int(request.data["state"][0]))
        profile.con_access_token = resp["access_token"]
        profile.con_refresh_token = resp["refresh_token"]
        profile.con_connected = True
        profile.con_access_expiry = datetime.now() + timedelta(minutes=50)
        profile.save()
        return Response(status=status.HTTP_200_OK)


