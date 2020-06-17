from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response

from .permissions import Check_API_KEY_Auth

class UserListView(APIView):
    permission_classes = [HasAPIKey]


class ExampleView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


def product_list(request):
	conn = http.client.HTTPConnection("api.rajaongkir.com")
	payload = "origin=501&destination=114&weight=1700&courier=jne"
	headers = {'key': settings.API_KEY_SECRET,'content-type': "application/x-www-form-urlencoded",}
	conn.request("POST", "/starter/cost", payload, headers)
	res = conn.getresponse()
	data = res.read()
	# print(data.decode("utf-8"))
	data =  data.decode("utf-8")

	
	
	pl = Product.objects.all()
	response = requests.get('https://api.kawalcorona.com/indonesia')
	api = response.json()
	context = {
		'products' : pl,
		'nama_negara': api[0]['name'],
		'positif':api[0]['positif'],
		'data':data,
	}
	template = 'shop/list.html'
	return render(request, template, context)