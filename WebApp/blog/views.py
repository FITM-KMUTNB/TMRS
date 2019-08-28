from django.views.generic import TemplateView
from django.shortcuts import render
import sys
sys.path.append('..')
from FindCentroid import calcentroid

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def post(self, request):
        query = request.POST.get("query")
        keyword, centroid = calcentroid(query)
        context = {'symptom' : keyword, 'disease' : centroid}
        return render(request, self.template_name, context)

