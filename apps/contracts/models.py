from django.db import models
from django.conf import settings

class Contract(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    parties_involved = models.JSONField()
    pdf_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contracts_contract'  # Explicitly set table name
        ordering = ['-created_at']

    def __str__(self):
        return self.title
