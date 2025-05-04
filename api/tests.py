from datetime import datetime, timezone
import pytest
import freezegun
from rest_framework.test import APIClient
from .factories import UserFactory, AnemometerFactory, WindSpeedReadingFactory
from .models import Anemometer, WindSpeedReading


# Create your tests here.


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def token(client, user, db):
    user.set_password('testpass')
    user.save()  # Ensure the password is hashed and user is saved
    response = client.post('/api/token/', {'username': user.username, 'password': 'testpass'})
    assert response.status_code == 200, response.content  # Ensure token request succeeds
    return response.data['access']

@pytest.mark.django_db
def test_anemometer_str_method():
    anemometer = AnemometerFactory(name='Test Anemometer')
    assert str(anemometer) == 'Test Anemometer'

@pytest.mark.django_db
def test_create_anemometer(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.post('/api/anemometers/', {'name': 'Test', 'latitude': 45.0, 'longitude': -93.0, 'tags': []})
    assert response.status_code == 201
    assert Anemometer.objects.count() == 1
    assert Anemometer.objects.get().name == 'Test'

@pytest.mark.django_db
def test_create_anemometer_without_authentication(client, token):
    response = client.post('/api/anemometers/', {'name': 'Test', 'latitude': 45.0, 'longitude': -93.0, 'tags': []})
    assert response.status_code == 401
    assert Anemometer.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_data, error_message",
    [
        (
            {
                'name': 'Test',
                'latitude': 'invalid',
                'longitude': -93.0,
                'tags': []
            },
            {'latitude': ['A valid number is required.']}
        ),
        (
            {
                'latitude': 45.0,
                'longitude': -93.0,
                'tags': []
            },
            {'name': ['This field is required.']}
        ),
    ]
)
def test_create_anemometer_invalid_data(client, token, invalid_data, error_message):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.post('/api/anemometers/', invalid_data)
    assert response.status_code == 400
    assert response.json() == error_message
    assert Anemometer.objects.count() == 0

@pytest.mark.django_db
def test_read_anemometer_list(client, token):
    AnemometerFactory.create_batch(5)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get('/api/anemometers/')
    assert response.status_code == 200
    assert len(response.json()['results']) == 5

@pytest.mark.django_db
def test_read_anemometer_filter_by_one_tag(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    AnemometerFactory(tags=['coastal'])
    response = client.get('/api/anemometers/?tags=coastal')
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert isinstance(response.json(), dict), response.json()
    assert response.json()['count'] == 1
    assert 'results' in response.json(), response.json()
    assert len(response.json()['results']) > 0
    assert all('coastal' in a['tags'] for a in response.json()['results'])

@pytest.mark.django_db
@freezegun.freeze_time(datetime(2025, 2, 22, 14, 6, 26, 484813, tzinfo=timezone.utc))
def test_read_anemometer_filter_by_tags():
    client = APIClient()
    user = UserFactory()
    user.set_password('testpass')
    user.save()  # Ensure the password is hashed and user is saved
    response = client.post('/api/token/', {'username': user.username, 'password': 'testpass'})
    assert response.status_code == 200, response.content  # Ensure token request succeeds
    token = response.data['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    AnemometerFactory(
        name='Anemometer 1',
        latitude=-29.0022675,
        longitude=-101.028684,
        tags=['coastal', "low-wind"],
    )
    AnemometerFactory(
        name='Anemometer 2',
        latitude=35.5340375,
        longitude=-122.46333,
        tags=['coastal', "high-wind"],
    )
    AnemometerFactory(
        name='Anemometer 3',
        latitude=23.750874,
        longitude=-75.512717,
        tags=['desert', "hot-weather"],
    )
    AnemometerFactory(
        name='Anemometer 4',
        latitude=35.5340375,
        longitude=-122.46333,
        tags=['desert', "high-wind"],
    )
    AnemometerFactory(
        name='Anemometer 5',
        latitude=35.5340375,
        longitude=-122.46333,
        tags=['mountain', "cold-weather"],
    )
    AnemometerFactory(
        name='Anemometer 6',
        latitude=35.5340375,
        longitude=-122.46333,
        tags=['urban', "modern-wind"],
    )
    response = client.get('/api/anemometers/?tags=coastal,high-wind')
    assert response.status_code == 200
    assert response.json()['count'] == 3
    assert response.json()['results'] == [
        {
           'created_at': '2025-02-22T14:06:26.484813Z',
            'daily_mean_speed': 0,
            'id': 1,
            'latest_readings': [],
           'latitude': -29.0022675,
           'longitude': -101.028684,
           'name': 'Anemometer 1',
            'tags': [
                'coastal',
                'low-wind',
            ],
            'weekly_mean_speed': 0,
        },
        {
           'created_at': '2025-02-22T14:06:26.484813Z',
            'daily_mean_speed': 0,
            'id': 2,
            'latest_readings': [],
           'latitude': 35.5340375,
           'longitude': -122.46333,
           'name': 'Anemometer 2',
            'tags': [
                'coastal',
                'high-wind',
            ],
            'weekly_mean_speed': 0,
        },
       {
           'created_at': '2025-02-22T14:06:26.484813Z',
           'daily_mean_speed': 0,
           'id': 4,
           'latest_readings': [],
           'latitude': 35.5340375,
           'longitude': -122.46333,
           'name': 'Anemometer 4',
           'tags': [
               'desert',
               'high-wind',
           ],
           'weekly_mean_speed': 0,
       },
    ]

@pytest.mark.django_db
def test_read_anemometer_by_name(client, token):
    AnemometerFactory(name='Test Anemometer')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(f'/api/anemometers/?search=Test')
    assert response.status_code == 200
    assert len(response.json()['results']) == 1

@pytest.mark.django_db
def test_read_one_anemometer(client, token):
    anemometer = AnemometerFactory()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(f'/api/anemometers/{anemometer.id}/')
    assert response.status_code == 200
    assert response.json()['name'] == anemometer.name

@pytest.mark.django_db
def test_update_anemometer(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    anemometer = AnemometerFactory()
    update_data = {'name': 'Updated Anemometer', 'latitude': anemometer.latitude, 'longitude': anemometer.longitude, 'tags': ['updated']}
    response = client.put(f'/api/anemometers/{anemometer.id}/', update_data, format='json')
    assert response.status_code == 200, response.content
    assert response.json()['name'] == 'Updated Anemometer'

@pytest.mark.django_db
def test_delete_anemometer(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    anemometer = AnemometerFactory()
    response = client.delete(f'/api/anemometers/{anemometer.id}/')
    assert response.status_code == 204
    response = client.get(f'/api/anemometers/{anemometer.id}/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_create_wind_speed(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Create an anemometer first
    anemometer = AnemometerFactory()
    
    # Now submit a wind speed reading for the created anemometer
    response = client.post('/api/readings/', {
        'anemometer': anemometer.id,
        'speed_knots': 12.5,
        'recorded_at': '2024-02-21T16:00:00Z'
    })
    assert response.status_code == 201
    assert WindSpeedReading.objects.count() == 1
    assert WindSpeedReading.objects.get().speed_knots == 12.5

@pytest.mark.django_db
def test_create_wind_speed_invalid_data(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.post('/api/readings/', {
        'anemometer': 1,
        'speed_knots': 'invalid',
        'recorded_at': '2024-02-21T16:00:00Z'
    })
    assert response.status_code == 400
    assert WindSpeedReading.objects.count() == 0
    assert response.json() == {
        'anemometer': ['Invalid pk "1" - object does not exist.'],
        'speed_knots': ['A valid number is required.']
    }

@pytest.mark.django_db
def test_wind_speed_statistics(client, token):
    anemometer = AnemometerFactory(latitude=34.0522, longitude=-118.2437)
    for speed in [10.0, 15.0, 20.0, 25.0, 30.0]:
        WindSpeedReadingFactory(anemometer=anemometer, speed_knots=speed)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/stats/?latitude=34.0522&longitude=-118.2437&radius=10')

    assert response.status_code == 200
    assert response.json() == {
        'max': 30.0,
        'mean': 20.0,
        'min': 10.0,
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_data, error_message",
    [
        (
            {},
            {
                'latitude': ['This field is required.'],
                'longitude': ['This field is required.'],
                'radius': ['This field is required.'],
            }
        ),
        (
            {
                'latitude': 45.0,
                'longitude': 'invalid',
                'radius': -10,
            },
            {
                'longitude': ['A valid number is required.'],
                'radius': ['Ensure this value is greater than or equal to 0.']
            }
        ),
    ]
)
def test_wind_speed_statistics_invalid_data(client, token, invalid_data, error_message):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get('/api/stats/', invalid_data)
    assert response.status_code == 400
    assert response.json() == error_message

@pytest.mark.django_db
@pytest.mark.parametrize("endpoint", [
    ("/api/anemometers/"),
    ("/api/readings/"),
    ("/api/stats/?latitude=34.0522&longitude=-118.2437&radius=10"),
])
def test_unauthorized_access(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication credentials were not provided."
