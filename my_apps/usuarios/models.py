from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return self.user.username
    


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Profile, through='Membership')

    def __str__(self):
        return self.name
    
    
class Membership(models.Model):
    
    
    class roleChoices(models.Choices):
        admin = 'admin'
        member = 'member'
    
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=roleChoices.choices,
        default=roleChoices.member
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'organization')

    def __str__(self):
        return f"{self.profile} - {self.organization} ({self.role})"