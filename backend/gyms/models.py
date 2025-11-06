import uuid
from django.db import models


class Sala(models.Model):
    """
    Model pentru săli de fitness
    Se afișează pe hartă cu iconiță ganteră
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nume = models.CharField(max_length=200, help_text="Numele sălii de fitness")
    adresa = models.CharField(max_length=300, help_text="Adresa completă a sălii")
    oras = models.CharField(max_length=100, blank=True, null=True, help_text="Orașul unde se află sala")
    descriere = models.TextField(blank=True, null=True, help_text="Descriere detaliată a sălii")
    facilitati = models.TextField(blank=True, null=True, help_text="Listă de facilități disponibile")
    latitudine = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitudine pentru hartă")
    longitudine = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitudine pentru hartă")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sala de Fitness"
        verbose_name_plural = "Săli de Fitness"
        ordering = ['nume']

    def __str__(self):
        return f"{self.nume} - {self.adresa}"
