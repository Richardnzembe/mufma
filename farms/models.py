from django.db import models
from accounts.models import User
from django.utils import timezone

# ==============================
# Crop Model
# ==============================
class Crop(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'farmer'})
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True, null=True)
    # Use callable timezone.now so the default is evaluated at instance creation time
    # Django's DateField will accept a datetime and convert to date portion
    planted_date = models.DateField(default=timezone.now)
    expected_harvest_date = models.DateField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True, help_text="Area in hectares")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.farmer.phone_number}"


# ==============================
# Crop Activity Model
# ==============================
class CropActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('planting', 'Planting'),
        ('watering', 'Watering'),
        ('fertilizing', 'Fertilizing'),
        ('harvesting', 'Harvesting'),
        ('pest_control', 'Pest Control'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.activity_type} - {self.crop.name} ({self.date.date()})"

    @property
    def is_overdue(self):
        return self.status == 'pending' and self.date < timezone.now()


# ==============================
# Animal Model
# ==============================
class Animal(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('pig', 'Pig'),
        ('chicken', 'Chicken'),
        ('other', 'Other'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'farmer'})
    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPE_CHOICES, default='cattle')
    birth_date = models.DateField(blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.animal_type}) - {self.farmer.phone_number}"


# ==============================
# Animal Activity Model
# ==============================
class AnimalActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('feeding', 'Feeding'),
        ('watering', 'Watering'),
        ('milking', 'Milking'),
        ('vaccination', 'Vaccination'),
        ('breeding', 'Breeding'),
        ('health_check', 'Health Check'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.activity_type} - {self.animal.name} ({self.date.date()})"

    @property
    def is_overdue(self):
        return self.status == 'pending' and self.date < timezone.now()
