from django_cron import CronJobBase, Schedule
from .models import Sesiune


class ArchiveExpiredSessionsCronJob(CronJobBase):
    """
    Cron job pentru arhivarea automată a sesiunilor expirate
    Rulează o dată pe oră
    """
    RUN_EVERY_MINS = 60  # Rulează la fiecare oră

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'workouts.archive_expired_sessions'  # Identificator unic

    def do(self):
        """
        Găsește și arhivează toate sesiunile expirate cu status 'activ'
        """
        sesiuni_active = Sesiune.objects.filter(status='activ')
        count = 0

        for sesiune in sesiuni_active:
            if sesiune.is_expired():
                sesiune.status = 'arhivat'
                sesiune.save(update_fields=['status'])
                count += 1

        return f"Arhivate {count} sesiuni expirate"
