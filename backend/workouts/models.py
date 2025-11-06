import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import UserProfile
from gyms.models import Sala


class Sesiune(models.Model):
    """
    Sesiune de antrenament activă la o sală
    Vizibilă pe hartă până la expirare/arhivare
    """
    STATUS_CHOICES = [
        ('activ', 'Activ'),
        ('expirat', 'Expirat'),
        ('arhivat', 'Arhivat'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sesiuni')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sesiuni')
    tip_antrenament = models.CharField(max_length=100, help_text="Ex: Cardio, Forță, CrossFit, etc.")
    interval_orar = models.CharField(max_length=100, help_text="Ex: 18:00 - 20:00")
    descriere = models.TextField(blank=True, null=True, help_text="Descriere opțională a sesiunii")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activ')

    data_creare = models.DateTimeField(auto_now_add=True)
    data_expirare = models.DateTimeField(help_text="Sesiunea devine expirată după această dată")

    class Meta:
        verbose_name = "Sesiune de Antrenament"
        verbose_name_plural = "Sesiuni de Antrenament"
        ordering = ['-data_creare']

    def __str__(self):
        return f"{self.user.nume} - {self.tip_antrenament} la {self.sala.nume}"

    def save(self, *args, **kwargs):
        """
        Auto-setează data_expirare dacă nu e setată (ex: 24h de la creare)
        """
        if not self.data_expirare:
            self.data_expirare = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        """
        Verifică dacă sesiunea a expirat
        """
        return timezone.now() > self.data_expirare

    def archive_if_expired(self):
        """
        Arhivează sesiunea dacă a expirat
        """
        if self.is_expired() and self.status == 'activ':
            self.status = 'arhivat'
            self.save(update_fields=['status'])


class Cerere(models.Model):
    """
    Cerere de a deveni gym buddy pentru o sesiune
    Owner-ul sesiunii poate accepta/refuza
    """
    STATUS_CHOICES = [
        ('pending', 'În așteptare'),
        ('acceptat', 'Acceptat'),
        ('refuzat', 'Refuzat'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sesiune = models.ForeignKey(Sesiune, on_delete=models.CASCADE, related_name='cereri')
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cereri_trimise')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    data_creare = models.DateTimeField(auto_now_add=True)
    data_raspuns = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Cerere Gym Buddy"
        verbose_name_plural = "Cereri Gym Buddy"
        ordering = ['-data_creare']
        unique_together = ['sesiune', 'applicant']  # Un user poate trimite o singură cerere per sesiune

    def __str__(self):
        return f"{self.applicant.nume} -> {self.sesiune.user.nume} ({self.status})"

    def accept(self):
        """
        Acceptă cererea
        """
        self.status = 'acceptat'
        self.data_raspuns = timezone.now()
        self.save()

    def reject(self):
        """
        Refuză cererea
        """
        self.status = 'refuzat'
        self.data_raspuns = timezone.now()
        self.save()
