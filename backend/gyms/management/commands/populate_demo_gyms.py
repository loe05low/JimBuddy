from django.core.management.base import BaseCommand
from gyms.models import Sala


class Command(BaseCommand):
    help = 'Populează baza de date cu săli demo de test'

    def handle(self, *args, **kwargs):
        """
        Adaugă săli demo în București
        Coordonate GPS pentru locații reale
        """
        demo_gyms = [
            {
                'nume': 'World Class Victoriei',
                'adresa': 'Bulevardul Lascăr Catargiu 15, București',
                'latitudine': 44.450569,
                'longitudine': 26.089380,
            },
            {
                'nume': 'GymBox Obor',
                'adresa': 'Bulevardul Ferdinand 30, București',
                'latitudine': 44.433109,
                'longitudine': 26.119509,
            },
            {
                'nume': 'Iron Gym Militari',
                'adresa': 'Strada Iuliu Maniu 7, București',
                'latitudine': 44.430231,
                'longitudine': 26.030428,
            },
            {
                'nume': 'Gold\'s Gym Universitate',
                'adresa': 'Bulevardul Regina Elisabeta 35, București',
                'latitudine': 44.435561,
                'longitudine': 26.097799,
            },
            {
                'nume': 'FitLife Unirii',
                'adresa': 'Piața Unirii 1, București',
                'latitudine': 44.426766,
                'longitudine': 26.102543,
            },
            {
                'nume': 'CrossFit Arena Pipera',
                'adresa': 'Șoseaua București-Ploiești 42D, București',
                'latitudine': 44.499031,
                'longitudine': 26.126897,
            },
            {
                'nume': 'PowerGym Timpuri Noi',
                'adresa': 'Bulevardul Timișoara 26, București',
                'latitudine': 44.413298,
                'longitudine': 26.074562,
            },
            {
                'nume': 'Body & Mind Fitness Herastrau',
                'adresa': 'Strada Aviator Popisteanu 54A, București',
                'latitudine': 44.474724,
                'longitudine': 26.082474,
            },
        ]

        created_count = 0
        updated_count = 0

        for gym_data in demo_gyms:
            sala, created = Sala.objects.get_or_create(
                nume=gym_data['nume'],
                defaults=gym_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creată: {sala.nume}')
                )
            else:
                # Actualizează dacă există deja
                for key, value in gym_data.items():
                    setattr(sala, key, value)
                sala.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'→ Actualizată: {sala.nume}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Finalizat! {created_count} săli create, {updated_count} actualizate.'
            )
        )
