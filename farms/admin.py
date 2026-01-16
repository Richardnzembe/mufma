from django.contrib import admin
from .models import Crop, CropActivity, Animal, AnimalActivity

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'planted_date', 'expected_harvest_date', 'area')
    search_fields = ('name', 'farmer__phone_number')

@admin.register(CropActivity)
class CropActivityAdmin(admin.ModelAdmin):
    list_display = ('crop', 'activity_type', 'date')
    search_fields = ('crop__name',)
    list_filter = ('activity_type',)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'farmer', 'birth_date', 'breed')
    search_fields = ('name', 'farmer__phone_number')
    list_filter = ('animal_type',)

@admin.register(AnimalActivity)
class AnimalActivityAdmin(admin.ModelAdmin):
    list_display = ('animal', 'activity_type', 'date')
    search_fields = ('animal__name',)
    list_filter = ('activity_type',)
