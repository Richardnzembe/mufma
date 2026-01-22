from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Crop, CropActivity, Animal, AnimalActivity
from datetime import date, timedelta
from django.utils import timezone

@login_required(login_url='/accounts/login/')
def home(request):
    crops = Crop.objects.filter(farmer=request.user)
    animals = Animal.objects.filter(farmer=request.user)
    return render(request, "farms/home.html", {"crops": crops, "animals": animals})


@login_required(login_url='/accounts/login/')
def add_crop(request):
    if request.method == "POST":
        name = request.POST.get("name")
        variety = request.POST.get("variety")
        area_str = request.POST.get("area")
        planted_date_str = request.POST.get("planted_date")
        expected_harvest_date_str = request.POST.get("expected_harvest_date")
        notes = request.POST.get("notes")

        if planted_date_str:
            planted_date = date.fromisoformat(planted_date_str)
        else:
            planted_date = timezone.now().date()

        if expected_harvest_date_str:
            expected_harvest_date = date.fromisoformat(expected_harvest_date_str)
        else:
            expected_harvest_date = planted_date + timedelta(days=90)

        area = float(area_str) if area_str else None

        crop = Crop.objects.create(
            name=name,
            variety=variety,
            area=area,
            farmer=request.user,
            planted_date=planted_date,
            expected_harvest_date=expected_harvest_date,
            notes=notes
        )
        return redirect("home")
    return render(request, "farms/add_crop.html")


@login_required(login_url='/accounts/login/')
def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    activities = crop.activities.all()
    return render(request, "farms/crop_detail.html", {"crop": crop, "activities": activities})


@login_required(login_url='/accounts/login/')
def add_activity(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    if request.method == "POST":
        activity_type = request.POST.get("activity_type")
        description = request.POST.get("description")
        CropActivity.objects.create(crop=crop, activity_type=activity_type, description=description)
        return redirect("farms:crop_detail", crop_id=crop.id)
    return render(request, "farms/add_activity.html", {"crop": crop})


@login_required(login_url='/accounts/login/')
def complete_task(request, task_id):
    task = get_object_or_404(CropActivity, id=task_id, crop__farmer=request.user)
    task.status = 'completed'
    task.save()
    return redirect("farms:crop_detail", crop_id=task.crop.id)


@login_required(login_url='/accounts/login/')
def delete_task(request, task_id):
    task = get_object_or_404(CropActivity, id=task_id, crop__farmer=request.user)
    crop_id = task.crop.id
    task.delete()
    return redirect("farms:crop_detail", crop_id=crop_id)


@login_required(login_url='/accounts/login/')
def timeline(request):
    crop_tasks = CropActivity.objects.filter(crop__farmer=request.user)
    animal_tasks = AnimalActivity.objects.filter(animal__farmer=request.user)
    tasks = list(crop_tasks) + list(animal_tasks)
    tasks.sort(key=lambda x: x.date)
    return render(request, "farms/timeline.html", {"tasks": tasks})


@login_required(login_url='/accounts/login/')
def add_animal(request):
    if request.method == "POST":
        name = request.POST.get("name")
        animal_type = request.POST.get("animal_type")
        other_animal_type = request.POST.get("other_animal_type")
        birth_date_str = request.POST.get("birth_date")
        breed = request.POST.get("breed")

        # If "other" is selected, use the custom animal type
        if animal_type == "other" and other_animal_type:
            animal_type = other_animal_type

        if birth_date_str:
            birth_date = date.fromisoformat(birth_date_str)
        else:
            birth_date = None

        animal = Animal.objects.create(
            name=name,
            animal_type=animal_type,
            farmer=request.user,
            birth_date=birth_date,
            breed=breed
        )
        return redirect("home")
    return render(request, "farms/add_animal.html")


@login_required(login_url='/accounts/login/')
def animal_detail(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, farmer=request.user)
    activities = animal.activities.all()
    return render(request, "farms/animal_detail.html", {"animal": animal, "activities": activities})


@login_required(login_url='/accounts/login/')
def add_animal_activity(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, farmer=request.user)
    if request.method == "POST":
        activity_type = request.POST.get("activity_type")
        custom_activity = request.POST.get("custom_activity")
        description = request.POST.get("description")
        
        # If "other" is selected, use the custom activity type
        if activity_type == "other" and custom_activity:
            activity_type = custom_activity
        
        AnimalActivity.objects.create(animal=animal, activity_type=activity_type, description=description)
        return redirect("farms:animal_detail", animal_id=animal.id)
    return render(request, "farms/add_animal_activity.html", {"animal": animal})


@login_required(login_url='/accounts/login/')
def complete_animal_task(request, task_id):
    task = get_object_or_404(AnimalActivity, id=task_id, animal__farmer=request.user)
    task.status = 'completed'
    task.save()
    return redirect("farms:animal_detail", animal_id=task.animal.id)


@login_required(login_url='/accounts/login/')
def delete_animal_task(request, task_id):
    task = get_object_or_404(AnimalActivity, id=task_id, animal__farmer=request.user)
    animal_id = task.animal.id
    task.delete()
    return redirect("farms:animal_detail", animal_id=animal_id)


@login_required(login_url='/accounts/login/')
def edit_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, farmer=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        animal_type = request.POST.get("animal_type")
        other_animal_type = request.POST.get("other_animal_type")
        birth_date_str = request.POST.get("birth_date")
        breed = request.POST.get("breed")
        notes = request.POST.get("notes")

        # If "other" is selected, use the custom animal type
        if animal_type == "other" and other_animal_type:
            animal_type = other_animal_type

        if birth_date_str:
            birth_date = date.fromisoformat(birth_date_str)
        else:
            birth_date = None

        animal.name = name
        animal.animal_type = animal_type
        animal.birth_date = birth_date
        animal.breed = breed
        animal.notes = notes
        animal.save()
        return redirect("farms:animal_detail", animal_id=animal.id)
    is_other = animal.animal_type not in ['cattle', 'sheep', 'goat', 'pig', 'chicken']
    context = {
        'animal': animal,
        'is_other': is_other,
        'other_value': animal.animal_type if is_other else '',
        'animal_type_value': 'other' if is_other else animal.animal_type,
    }
    return render(request, "farms/edit_animal.html", context)


@login_required(login_url='/accounts/login/')
def delete_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, farmer=request.user)
    if request.method == "POST":
        animal.delete()
        return redirect("farms:home")
    return render(request, "farms/delete_animal.html", {"animal": animal})


@login_required(login_url='/accounts/login/')
def edit_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        variety = request.POST.get("variety")
        area_str = request.POST.get("area")
        planted_date_str = request.POST.get("planted_date")
        expected_harvest_date_str = request.POST.get("expected_harvest_date")
        notes = request.POST.get("notes")

        if planted_date_str:
            planted_date = date.fromisoformat(planted_date_str)
        else:
            planted_date = timezone.now().date()

        if expected_harvest_date_str:
            expected_harvest_date = date.fromisoformat(expected_harvest_date_str)
        else:
            expected_harvest_date = planted_date + timedelta(days=90)

        area = float(area_str) if area_str else None

        crop.name = name
        crop.variety = variety
        crop.area = area
        crop.planted_date = planted_date
        crop.expected_harvest_date = expected_harvest_date
        crop.notes = notes
        crop.save()
        return redirect("farms:crop_detail", crop_id=crop.id)
    return render(request, "farms/edit_crop.html", {"crop": crop})


@login_required(login_url='/accounts/login/')
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    if request.method == "POST":
        crop.delete()
        return redirect("farms:home")
    return render(request, "farms/delete_crop.html", {"crop": crop})


@login_required(login_url='/accounts/login/')
def animals_by_type(request, animal_type):
    animals = Animal.objects.filter(farmer=request.user, animal_type=animal_type)
    return render(request, "farms/animals_by_type.html", {"animals": animals, "animal_type": animal_type})


def offline(request):
    """Simple offline fallback page used by the service worker."""
    return render(request, "offline.html")
