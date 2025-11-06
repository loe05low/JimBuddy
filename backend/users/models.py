from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Profil utilizator - extinde Django User model
    Câmpuri: nume, poză, rating, nr_antrenamente, grad
    """

    GRAD_CHOICES = [
        ('Începător', 'Începător'),
        ('Intermediar', 'Intermediar'),
        ('Avansat', 'Avansat'),
        ('Sportiv', 'Sportiv'),
        ('Expert', 'Expert'),
        ('Veteran', 'Veteran'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nume = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Poza de profil")
    bio = models.CharField(max_length=140, blank=True, null=True, help_text="Bio scurt (max 140 caractere)")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="Oraș")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Număr de telefon")
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=5.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        help_text="Rating mediu 1-5 stele"
    )
    nr_antrenamente = models.IntegerField(default=0, help_text="Număr total de antrenamente completate")
    grad = models.CharField(max_length=20, choices=GRAD_CHOICES, default='Începător')
    current_streak = models.IntegerField(default=0, help_text="Număr de zile consecutive cu antrenament")
    last_workout_date = models.DateField(blank=True, null=True, help_text="Data ultimului antrenament completat")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Utilizator"
        verbose_name_plural = "Profile Utilizatori"

    def __str__(self):
        return f"{self.nume} ({self.grad}) - Rating: {self.rating}"

    def update_rating(self):
        """
        Recalculează rating-ul mediu bazat pe toate rating-urile primite
        """
        from ratings.models import Rating
        ratings = Rating.objects.filter(to_user=self)
        if ratings.exists():
            avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = round(avg_rating, 1)
            self.save(update_fields=['rating'])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creează automat un profil când se creează un User nou
    """
    if created:
        UserProfile.objects.create(
            user=instance,
            nume=instance.username  # Default la username, poate fi schimbat
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Salvează profilul când se salvează User-ul
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


class BlockedUser(models.Model):
    """
    Model pentru utilizatori blocați
    Un user poate bloca alți utilizatori
    """
    blocker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blocked_by')
    reason = models.TextField(blank=True, null=True, help_text="Motiv blocare")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Utilizator Blocat"
        verbose_name_plural = "Utilizatori Blocați"
        unique_together = ['blocker', 'blocked']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.blocker.nume} blocked {self.blocked.nume}"
