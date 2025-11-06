from django.db.models.signals import post_save
from django.dispatch import receiver
from workouts.models import Cerere
from ratings.models import Rating
from .models import Notification


@receiver(post_save, sender=Cerere)
def create_request_notification(sender, instance, created, **kwargs):
    """
    Create notification when a buddy request is created or updated
    """
    if created:
        # New request notification for session owner
        Notification.objects.create(
            user=instance.sesiune.user,
            tip='cerere_noua',
            titlu='New Buddy Request',
            mesaj=f'{instance.applicant.nume} wants to be your gym buddy for "{instance.sesiune.tip_antrenament}" session',
            link=f'/profile'  # Link to requests tab
        )
    elif instance.status in ['acceptat', 'refuzat']:
        # Request accepted/rejected notification for applicant
        tip = 'cerere_acceptata' if instance.status == 'acceptat' else 'cerere_refuzata'
        titlu = 'Request Accepted! 🎉' if instance.status == 'acceptat' else 'Request Declined'
        mesaj = (
            f'{instance.sesiune.user.nume} accepted your buddy request!' if instance.status == 'acceptat'
            else f'{instance.sesiune.user.nume} declined your buddy request'
        )

        Notification.objects.create(
            user=instance.applicant,
            tip=tip,
            titlu=titlu,
            mesaj=mesaj,
            link=f'/profile'
        )


@receiver(post_save, sender=Rating)
def create_rating_notification(sender, instance, created, **kwargs):
    """
    Create notification when user receives a new rating
    """
    if created:
        stars = '⭐' * int(instance.rating)
        Notification.objects.create(
            user=instance.to_user,
            tip='rating_nou',
            titlu='New Rating Received!',
            mesaj=f'{instance.from_user.nume} rated you {stars} ({instance.rating}/5.0)',
            link=f'/profile'  # Link to ratings tab
        )
