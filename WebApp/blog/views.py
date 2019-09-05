from django.views.generic import TemplateView
from django.shortcuts import render
import sys
sys.path.append('..')
import FindCentroid as fc

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def post(self, request):
        query = request.POST.get("query")
        keyword, allcentroid, topdisease = fc.Centroid(query)
        context = {'symptom' : keyword, 'centroid' : allcentroid, 'disease' : topdisease}
        return render(request, self.template_name, context)

