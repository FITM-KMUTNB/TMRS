from django.views.generic import TemplateView
from django.shortcuts import render
import sys
sys.path.append('..')
import FindCentroid as fc

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def post(self, request):
        query = request.POST.get("query")
        allcentroid, diseasecentroid = fc.Centroid(query)
        #context = {'symptom' : keyword, 'disease' : disease, 'centroid' : centroid}
        #return render(request, self.template_name, context)

