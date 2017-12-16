from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.views import APIView
import requests
from rest_framework.response import Response

from googlemaps import settings


def index(request):
    context = {
        'key': 'value'
    }
    return render(request, 'maps/index.html', context)


class ReverseGeocode(APIView):
    def get(self, request, lat, lng):
        try:
            return Response(reverse_geo_code(lat,lng))
        except Exception as exp:
            return Response({'status':'failure'})

def reverse_geo_code(lat,lng):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'.format(lat,lng,settings.google_map_key)
    resp = requests.post(url)
    street_address = fetch_address(resp.json(), type='route')
    postal_code = fetch_address(resp.json(), type = 'postal_code')
    state = fetch_address(resp.json(), type='administrative_area_level_1')
    country = fetch_address(resp.json(), type='country')
    city = fetch_address(resp.json(), type='administrative_area_level_2')
    return {
        'lat':lat,
        'lng':lng,
        'streetAddress':street_address,
        'zipCode': postal_code,
        'state': state,
        'country': country,
        'city':city
    }


def fetch_address(address_json, type):
    for each in address_json.get('results'):
        if type in each.get('address_components')[0].get('types'):
            long_name =  each.get('address_components')[0].get('long_name')
            short_name = each.get('address_components')[0].get('short_name')
            if not long_name:
                return short_name
            return long_name
