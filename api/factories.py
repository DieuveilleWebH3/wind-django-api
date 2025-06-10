import factory
from django.contrib.auth.models import User
from .models import Anemometer, WindSpeedReading


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Ensure the user is saved properly

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass")


class AnemometerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Anemometer

    name = factory.Sequence(lambda n: f"Anemometer {n}")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    tags = factory.LazyFunction(lambda: ["test"])


class WindSpeedReadingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WindSpeedReading

    anemometer = factory.SubFactory(AnemometerFactory)
    speed_knots = factory.Faker(
        "random_float", left_digits=2, right_digits=1, positive=True
    )
    recorded_at = factory.Faker("date_time_this_year")
