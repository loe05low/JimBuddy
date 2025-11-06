from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserProfile
from workouts.models import Sesiune


class Rating(models.Model):
    """
    Rating și comentariu dat după finalizarea unui antrenament
    Rating: 1-5 stele
    Comentarii ordonate descrescător după dată
    """
    from_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='ratings_date'
    )
    to_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='ratings_primite'
    )
    sesiune = models.ForeignKey(Sesiune, on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        help_text="Rating 1-5 stele"
    )
    comentariu = models.TextField(blank=True, null=True, help_text="Comentariu opțional despre partener")

    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Rating-uri"
        ordering = ['-data']  # Descrescător după dată (cele mai recente primele)
        unique_together = ['from_user', 'to_user', 'sesiune']  # Un user poate da un singur rating per sesiune

    def __str__(self):
        return f"{self.from_user.nume} → {self.to_user.nume}: {self.rating}★"


@receiver(post_save, sender=Rating)
def update_user_rating(sender, instance, created, **kwargs):
    """
    După adăugarea unui rating nou, recalculează rating-ul mediu al user-ului
    și incrementează nr_antrenamente
    """
    if created:
        # Recalculează rating-ul mediu
        instance.to_user.update_rating()

        # Incrementează numărul de antrenamente pentru ambii utilizatori
        instance.from_user.nr_antrenamente += 1
        instance.from_user.save(update_fields=['nr_antrenamente'])

        instance.to_user.nr_antrenamente += 1
        instance.to_user.save(update_fields=['nr_antrenamente'])
