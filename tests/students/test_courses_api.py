import pytest
from rest_framework.test import APIClient
from students.models import Course
from model_bakery import baker
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user('admin')

@pytest.fixture
def course_factory():
    def courses_make(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return courses_make

@pytest.mark.django_db
def test_courses(client, user, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/courses/6', content_type='application/json')
    data = response.json()
    assert response.status_code == 200
    assert courses[6].name == data['name']
