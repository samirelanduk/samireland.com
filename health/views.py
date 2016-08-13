from django.shortcuts import render, redirect
from health.forms import MuscleGroupForm

# Create your views here.
def edit_page(request):
    if request.method == "POST":
        group_form = MuscleGroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
        return redirect("/health/edit/")
    group_form = MuscleGroupForm()
    return render(request, "edit_health.html", {"group_form": group_form})
