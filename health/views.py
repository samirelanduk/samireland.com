from django.shortcuts import render, redirect
from django.http import Http404
from health.forms import MuscleGroupForm
from health.models import MuscleGroup

# Create your views here.
def edit_page(request):
    if request.method == "POST":
        group_form = MuscleGroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            return redirect("/health/edit/")
        else:
            muscle_groups = MuscleGroup.objects.all().order_by("name")
            return render(request, "edit_health.html", {
             "group_form": group_form, "muscle_groups": muscle_groups
            })
    muscle_groups = MuscleGroup.objects.all().order_by("name")
    group_form = MuscleGroupForm()
    return render(request, "edit_health.html", {
     "group_form": group_form, "muscle_groups": muscle_groups
    })


def musclegroup_page(request, name):
    try:
        group = MuscleGroup.objects.get(name=name)
    except MuscleGroup.DoesNotExist:
        raise Http404()
    if request.method == "POST":
        form = MuscleGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("/health/edit/musclegroup/%s/" % request.POST["name"])
        else:
            return redirect("/health/edit/musclegroup/%s/" % group.name)
    form = MuscleGroupForm()
    return render(request, "musclegroup.html", {"group": group, "form": form})


def musclegroup_delete_page(request, name):
    try:
        group = MuscleGroup.objects.get(name=name)
    except MuscleGroup.DoesNotExist:
        raise Http404()
    if request.method == "POST":
        group.delete()
        return redirect("/health/edit/")
    return render(request, "musclegroup_delete.html", {"group": group})
