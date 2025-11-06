from django.core.management.base import BaseCommand
from gyms.models import Sala


class Command(BaseCommand):
    help = 'Populează baza de date cu săli de fitness din România'

    def handle(self, *args, **kwargs):
        # Șterge sălile existente (optional - comentează dacă vrei să păstrezi datele vechi)
        # Sala.objects.all().delete()
        # self.stdout.write(self.style.WARNING('Șters săli existente'))

        gyms_data = [
            # BUCUREȘTI
            {
                'nume': 'World Class Pipera',
                'adresa': 'Bd. Pipera 1A, București',
                'oras': 'București',
                'descriere': 'Cea mai mare sală de fitness din România, echipamente premium, piscină olimpică',
                'latitudine': 44.4917,
                'longitudine': 26.1257,
                'facilitati': 'Sală fitness, Piscină, Saună, Masaj, Grupate, Personal trainer'
            },
            {
                'nume': 'World Class Cotroceni',
                'adresa': 'Bd. Vasile Milea 4, București',
                'oras': 'București',
                'descriere': 'Locație premium în Mega Mall, echipamente de ultimă generație',
                'latitudine': 44.4366,
                'longitudine': 26.0489,
                'facilitati': 'Sală fitness, Piscină, Saună, Yoga, Pilates, Grupate'
            },
            {
                'nume': 'World Class Băneasa',
                'adresa': 'Șos. Bucuresti-Ploiești 42D, București',
                'oras': 'București',
                'descriere': 'Club exclusivist cu piscină semi-olimpică și echipamente premium',
                'latitudine': 44.5122,
                'longitudine': 26.0822,
                'facilitati': 'Sală fitness, Piscină, Saună, Masaj, Spa, Grupate'
            },
            {
                'nume': 'Flex Gym Universitate',
                'adresa': 'Bd. Regina Elisabeta 5-7, București',
                'oras': 'București',
                'descriere': 'Sală modernă în centrul Bucureștiului, echipamente Technogym',
                'latitudine': 44.4361,
                'longitudine': 26.0975,
                'facilitati': 'Sală fitness, Grupate, Personal trainer, Vestiare moderne'
            },
            {
                'nume': 'GymBox Titan',
                'adresa': 'Str. Camil Ressu 10, București',
                'oras': 'București',
                'descriere': 'Sală de cartier cu atmosferă prietenoasă, prețuri accesibile',
                'latitudine': 44.4422,
                'longitudine': 26.1733,
                'facilitati': 'Sală fitness, Grupate, CrossFit, Box'
            },
            {
                'nume': 'Fit Point Unirii',
                'adresa': 'Bd. Corneliu Coposu 5, București',
                'oras': 'București',
                'descriere': 'Sală compactă și modernă lângă Piața Unirii',
                'latitudine': 44.4265,
                'longitudine': 26.1031,
                'facilitati': 'Sală fitness, Grupate, Saună'
            },
            {
                'nume': 'Premium Gym Vitan',
                'adresa': 'Calea Vitan 55-59, București',
                'oras': 'București',
                'descriere': 'Sală premium cu echipamente profesionale',
                'latitudine': 44.4122,
                'longitudine': 26.1253,
                'facilitati': 'Sală fitness, CrossFit, Functional training, Saună'
            },

            # CLUJ-NAPOCA
            {
                'nume': 'World Class Iulius Mall Cluj',
                'adresa': 'Str. Alexandru Vaida Voevod 53B, Cluj-Napoca',
                'oras': 'Cluj-Napoca',
                'descriere': 'Cel mai mare club World Class din Cluj, cu piscină și spa',
                'latitudine': 46.7692,
                'longitudine': 23.5686,
                'facilitati': 'Sală fitness, Piscină, Spa, Saună, Grupate, Yoga'
            },
            {
                'nume': 'Fit Evolution Cluj',
                'adresa': 'Str. Aurel Vlaicu 2-4, Cluj-Napoca',
                'oras': 'Cluj-Napoca',
                'descriere': 'Sală modernă în centrul Clujului cu echipamente premium',
                'latitudine': 46.7712,
                'longitudine': 23.5989,
                'facilitati': 'Sală fitness, Grupate, Personal trainer, Vestiare'
            },
            {
                'nume': 'Body Concept Mănăștur',
                'adresa': 'Str. Mănăștur 2, Cluj-Napoca',
                'oras': 'Cluj-Napoca',
                'descriere': 'Sală populară în cartierul Mănăștur',
                'latitudine': 46.7558,
                'longitudine': 23.5503,
                'facilitati': 'Sală fitness, Grupate, CrossFit'
            },
            {
                'nume': 'Oxygen Gym Cluj',
                'adresa': 'Calea Turzii 216, Cluj-Napoca',
                'oras': 'Cluj-Napoca',
                'descriere': 'Sală dedicată antrenamentelor intense și culturism',
                'latitudine': 46.7868,
                'longitudine': 23.6236,
                'facilitati': 'Sală fitness, Culturism, Personal trainer'
            },

            # TIMIȘOARA
            {
                'nume': 'World Class Iulius Mall Timișoara',
                'adresa': 'Str. Aristide Demetriade 1, Timișoara',
                'oras': 'Timișoara',
                'descriere': 'Club premium cu vedere panoramică și echipamente de top',
                'latitudine': 45.7467,
                'longitudine': 21.2272,
                'facilitati': 'Sală fitness, Piscină, Saună, Spa, Grupate'
            },
            {
                'nume': 'Fit Class Timișoara',
                'adresa': 'Bd. Liviu Rebreanu 222, Timișoara',
                'oras': 'Timișoara',
                'descriere': 'Sală modernă cu atmosferă plăcută',
                'latitudine': 45.7489,
                'longitudine': 21.2403,
                'facilitati': 'Sală fitness, Grupate, Yoga, Pilates'
            },
            {
                'nume': 'Premium Gym Bega',
                'adresa': 'Str. Mitropolit Andrei Șaguna 3, Timișoara',
                'oras': 'Timișoara',
                'descriere': 'Sală boutique lângă râul Bega',
                'latitudine': 45.7597,
                'longitudine': 21.2267,
                'facilitati': 'Sală fitness, Personal trainer, Saună'
            },

            # IAȘI
            {
                'nume': 'World Class Palas Iași',
                'adresa': 'Bd. Carol I 11, Iași',
                'oras': 'Iași',
                'descriere': 'Club premium în cel mai exclusivist mall din Iași',
                'latitudine': 47.1585,
                'longitudine': 27.5878,
                'facilitati': 'Sală fitness, Piscină, Spa, Saună, Grupate'
            },
            {
                'nume': 'Fit Station Iași',
                'adresa': 'Str. Păcurari 121, Iași',
                'oras': 'Iași',
                'descriere': 'Sală modernă cu echipamente profesionale',
                'latitudine': 47.1667,
                'longitudine': 27.5833,
                'facilitati': 'Sală fitness, Grupate, CrossFit'
            },
            {
                'nume': 'GymBox Iași Copou',
                'adresa': 'Bd. Carol I 26, Iași',
                'oras': 'Iași',
                'descriere': 'Sală pentru studenți și tineri profesioniști',
                'latitudine': 47.1764,
                'longitudine': 27.5706,
                'facilitati': 'Sală fitness, Grupate, Box'
            },

            # CONSTANȚA
            {
                'nume': 'World Class City Park Mall',
                'adresa': 'Bd. Aurel Vlaicu 155, Constanța',
                'oras': 'Constanța',
                'descriere': 'Cel mai mare club de fitness din Constanța',
                'latitudine': 44.1917,
                'longitudine': 28.6328,
                'facilitati': 'Sală fitness, Piscină, Spa, Saună, Grupate'
            },
            {
                'nume': 'Sea Fitness Mamaia',
                'adresa': 'Bd. Mamaia 255, Constanța',
                'oras': 'Constanța',
                'descriere': 'Sală cu vedere la mare, atmosferă unică',
                'latitudine': 44.2317,
                'longitudine': 28.6072,
                'facilitati': 'Sală fitness, Grupate pe plajă, Yoga'
            },

            # BRAȘOV
            {
                'nume': 'World Class Coresi Shopping Resort',
                'adresa': 'Str. Zaharia Stancu 1, Brașov',
                'oras': 'Brașov',
                'descriere': 'Club modern cu vedere spre munți',
                'latitudine': 45.6408,
                'longitudine': 25.6106,
                'facilitati': 'Sală fitness, Piscină, Saună, Grupate'
            },
            {
                'nume': 'Fit Arena Brașov',
                'adresa': 'Bd. Eroilor 7-9, Brașov',
                'oras': 'Brașov',
                'descriere': 'Sală complet echipată în centrul orașului',
                'latitudine': 45.6564,
                'longitudine': 25.6089,
                'facilitati': 'Sală fitness, Grupate, CrossFit'
            },

            # CRAIOVA
            {
                'nume': 'World Class Electroputere Mall',
                'adresa': 'Bd. Decebal 1, Craiova',
                'oras': 'Craiova',
                'descriere': 'Club premium în cel mai mare mall din Craiova',
                'latitudine': 44.3167,
                'longitudine': 23.8147,
                'facilitati': 'Sală fitness, Piscină, Spa, Grupate'
            },
            {
                'nume': 'PowerGym Craiova',
                'adresa': 'Str. Brestei 24, Craiova',
                'oras': 'Craiova',
                'descriere': 'Sală dedicată antrenamentelor de forță',
                'latitudine': 44.3247,
                'longitudine': 23.7972,
                'facilitati': 'Sală fitness, Culturism, PowerLifting'
            },

            # GALAȚI
            {
                'nume': 'Fit Point Galați Mall',
                'adresa': 'Str. Brăilei 212, Galați',
                'oras': 'Galați',
                'descriere': 'Sală modernă în centrul comercial',
                'latitudine': 45.4353,
                'longitudine': 28.0578,
                'facilitati': 'Sală fitness, Grupate, Saună'
            },
            {
                'nume': 'GymBox Dunărea',
                'adresa': 'Bd. Dunărea 47, Galați',
                'oras': 'Galați',
                'descriere': 'Sală cu preturi accesibile și atmosferă prietenoasă',
                'latitudine': 45.4356,
                'longitudine': 28.0489,
                'facilitati': 'Sală fitness, Grupate'
            },

            # PLOIEȘTI
            {
                'nume': 'World Class Ploiești Shopping City',
                'adresa': 'Bd. Timișoara 1, Ploiești',
                'oras': 'Ploiești',
                'descriere': 'Club premium cu toate facilitățile',
                'latitudine': 44.9614,
                'longitudine': 26.0178,
                'facilitati': 'Sală fitness, Piscină, Saună, Grupate'
            },
            {
                'nume': 'Fit Evolution Ploiești',
                'adresa': 'Bd. Republicii 123, Ploiești',
                'oras': 'Ploiești',
                'descriere': 'Sală în centrul orașului',
                'latitudine': 44.9433,
                'longitudine': 26.0236,
                'facilitati': 'Sală fitness, Grupate'
            },

            # ORADEA
            {
                'nume': 'World Class Lotus Center',
                'adresa': 'Calea Clujului 1, Oradea',
                'oras': 'Oradea',
                'descriere': 'Cel mai mare club din Oradea',
                'latitudine': 47.0722,
                'longitudine': 21.9197,
                'facilitati': 'Sală fitness, Piscină, Spa, Grupate'
            },
            {
                'nume': 'FitZone Oradea',
                'adresa': 'Str. Republicii 14, Oradea',
                'oras': 'Oradea',
                'descriere': 'Sală boutique în centru',
                'latitudine': 47.0458,
                'longitudine': 21.9189,
                'facilitati': 'Sală fitness, Grupate, Yoga'
            },

            # SIBIU
            {
                'nume': 'Fit Life Sibiu',
                'adresa': 'Calea Dumbrăvii 121-131, Sibiu',
                'oras': 'Sibiu',
                'descriere': 'Sală modernă în cel mai mare mall din Sibiu',
                'latitudine': 45.7853,
                'longitudine': 24.1361,
                'facilitati': 'Sală fitness, Grupate, Saună'
            },
            {
                'nume': 'Premium Gym Sibiu',
                'adresa': 'Str. Nicolae Bălcescu 43, Sibiu',
                'oras': 'Sibiu',
                'descriere': 'Sală boutique în centrul istoric',
                'latitudine': 45.7967,
                'longitudine': 24.1519,
                'facilitati': 'Sală fitness, Personal trainer'
            },

            # BACĂU
            {
                'nume': 'World Class Bacău',
                'adresa': 'Str. Milcov 3, Bacău',
                'oras': 'Bacău',
                'descriere': 'Club premium cu piscină',
                'latitudine': 46.5758,
                'longitudine': 26.9142,
                'facilitati': 'Sală fitness, Piscină, Saună, Grupate'
            },
            {
                'nume': 'GymPoint Bacău',
                'adresa': 'Str. Republicii 165, Bacău',
                'oras': 'Bacău',
                'descriere': 'Sală accesibilă în centru',
                'latitudine': 46.5667,
                'longitudine': 26.9047,
                'facilitati': 'Sală fitness, Grupate'
            },

            # ARAD
            {
                'nume': 'Fit Class Arad Plaza',
                'adresa': 'Calea Aurel Vlaicu 297, Arad',
                'oras': 'Arad',
                'descriere': 'Sală modernă în centrul comercial',
                'latitudine': 46.1858,
                'longitudine': 21.3183,
                'facilitati': 'Sală fitness, Grupate, Saună'
            },
            {
                'nume': 'PowerZone Arad',
                'adresa': 'Bd. Revoluției 89, Arad',
                'oras': 'Arad',
                'descriere': 'Sală pentru antrenamente intense',
                'latitudine': 46.1764,
                'longitudine': 21.3122,
                'facilitati': 'Sală fitness, CrossFit, Culturism'
            },

            # PITEȘTI
            {
                'nume': 'Fit Arena Pitești Mall',
                'adresa': 'Calea Craiovei 93, Pitești',
                'oras': 'Pitești',
                'descriere': 'Sală modernă cu echipamente de top',
                'latitudine': 44.8478,
                'longitudine': 24.8675,
                'facilitati': 'Sală fitness, Grupate, Saună'
            },
            {
                'nume': 'GymBox Pitești',
                'adresa': 'Bd. Republicii 56, Pitești',
                'oras': 'Pitești',
                'descriere': 'Sală cu atmosferă prietenoasă',
                'latitudine': 44.8561,
                'longitudine': 24.8689,
                'facilitati': 'Sală fitness, Grupate'
            },

            # TÂRGU MUREȘ
            {
                'nume': 'World Class Plaza Romania',
                'adresa': 'Str. Gheorghe Doja 43, Târgu Mureș',
                'oras': 'Târgu Mureș',
                'descriere': 'Club premium în centrul orașului',
                'latitudine': 46.5425,
                'longitudine': 24.5639,
                'facilitati': 'Sală fitness, Piscină, Saună, Grupate'
            },

            # SUCEAVA
            {
                'nume': 'Fit Point Suceava',
                'adresa': 'Bd. 1 Mai 5, Suceava',
                'oras': 'Suceava',
                'descriere': 'Sală modernă cu echipamente complete',
                'latitudine': 47.6514,
                'longitudine': 26.2597,
                'facilitati': 'Sală fitness, Grupate, Saună'
            },

            # BAIA MARE
            {
                'nume': 'FitZone Baia Mare',
                'adresa': 'Bd. Unirii 15, Baia Mare',
                'oras': 'Baia Mare',
                'descriere': 'Sală completă în centrul orașului',
                'latitudine': 47.6569,
                'longitudine': 23.5681,
                'facilitati': 'Sală fitness, Grupate, CrossFit'
            },
        ]

        created_count = 0
        updated_count = 0

        for gym_info in gyms_data:
            sala, created = Sala.objects.update_or_create(
                nume=gym_info['nume'],
                oras=gym_info['oras'],
                defaults={
                    'adresa': gym_info['adresa'],
                    'descriere': gym_info['descriere'],
                    'latitudine': gym_info['latitudine'],
                    'longitudine': gym_info['longitudine'],
                    'facilitati': gym_info['facilitati'],
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {sala.nume} - {sala.oras}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {sala.nume} - {sala.oras}')
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS(f'TOTAL: {created_count} săli create, {updated_count} săli actualizate'))
        self.stdout.write(self.style.SUCCESS(f'Total săli în database: {Sala.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Afișează statistici pe orașe
        self.stdout.write(self.style.SUCCESS('Statistici pe orașe:'))
        self.stdout.write(self.style.SUCCESS('-' * 70))

        from django.db.models import Count
        city_stats = Sala.objects.values('oras').annotate(count=Count('id')).order_by('-count')

        for stat in city_stats:
            self.stdout.write(f"  {stat['oras']}: {stat['count']} săli")

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Săli de fitness din România adăugate cu succes!'))
