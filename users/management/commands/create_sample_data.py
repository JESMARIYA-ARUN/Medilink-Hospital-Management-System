from django.core.management.base import BaseCommand
from users.models import CustomUser
import random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Sample lists
        names = ["John", "Emma", "David", "Sophia", "Liam", "Olivia", "Noah", "Ava", "James", "Mia"]

        # Create sample patients
        for i in range(10):
            name = random.choice(names)
            user = CustomUser.objects.create_user(
                username=f"patient{i}",
                password="patient123",
                first_name=name,
                role="patient",
            )
            print(f"Created Patient: {user.username}")

        # Create sample doctors
        for i in range(10):
            name = random.choice(names)
            user = CustomUser.objects.create_user(
                username=f"doctor{i}",
                password="doctor123",
                first_name=name,
                role="doctor"
            )
            print(f"Created Doctor: {user.username}")

        self.stdout.write(self.style.SUCCESS("Sample doctors and patients created successfully!"))
