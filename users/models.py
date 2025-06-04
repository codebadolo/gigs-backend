# users/models.py
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crée et sauvegarde un utilisateur avec un email et un mot de passe.
        """
        if not email:
            raise ValueError('L\'adresse email doit être renseignée')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et sauvegarde un super-utilisateur.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('buyer', 'Acheteur'),
        ('seller', 'Vendeur'),
        ('admin', 'Administrateur'),
    )

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    # Infos profil enrichies
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=255, blank=True, help_text="Langues parlées, séparées par des virgules")
    skills = models.CharField(max_length=500, blank=True, help_text="Compétences clés séparées par des virgules")
    hourly_rate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    available_for_hire = models.BooleanField(default=True)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)

    # Statistiques (à mettre à jour via signaux ou tâches)
    total_gigs = models.PositiveIntegerField(default=0)
    total_orders_completed = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Permissions et statut
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # accès admin Django
    date_joined = models.DateTimeField(default=timezone.now)

    
    # skills 
    # 
    skills = models.ManyToManyField(Skill, blank=True, related_name='users')
    # Manager personnalisé
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email obligatoire, username optionnel

    def __str__(self):
        return self.email


class Subscription(models.Model):
    SUBSCRIPTION_TYPES = (
        ('free', 'Gratuit'),
        ('premium', 'Premium'),
    )
    STATUS_CHOICES = (
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('cancelled', 'Annulé'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='free')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.email} - {self.type} ({self.status})"
