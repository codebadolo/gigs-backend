# marketplace/models.py
from django.db import models
from users.models import User

class Gig(models.Model):
    VISIBILITY_CHOICES = (
        ('standard', 'Standard'),
        ('sponsored', 'Sponsorisé'),
    )
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.IntegerField(help_text="Délai en jours")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=100)
    visibility_level = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='standard')
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'En cours'),
        ('delivered', 'Livré'),
        ('cancelled', 'Annulé'),
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('refunded', 'Remboursé'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_made')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

class Promotion(models.Model):
    PROMOTION_TYPES = (
        ('sponsored', 'Sponsorisé'),
        ('badge', 'Badge'),
    )
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='promotions')
    type = models.CharField(max_length=20, choices=PROMOTION_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Dispute(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputes_raised')
    description = models.TextField()
    status = models.CharField(max_length=20, default='open')
    resolution_date = models.DateTimeField(null=True, blank=True)
