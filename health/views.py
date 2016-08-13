from django.shortcuts import render
from health.forms import MuscleGroupForm

# Create your views here.
def edit_page(request):
    group_form = MuscleGroupForm()
    return render(request, "edit_health.html", {"group_form": group_form})
