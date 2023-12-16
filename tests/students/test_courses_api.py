import pytest
from rest_framework.test import APIClient
from students.models import Course
from model_bakery import baker
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def courses_make(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return courses_make

@pytest.mark.django_db
def test_courses_one(client, course_factory):
    courses = course_factory(_quantity=10)
    product = 1
    response = client.get(f'/courses/{product}/', content_type='application/json')
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == courses[product - 1].name

@pytest.mark.django_db
def test_courses_list(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/courses/', content_type='application/json')
    data = response.json()
    assert response.status_code == 200
    assert data == [model_to_dict(course) for course in courses]

@pytest.mark.django_db
def test_courses_id(client, course_factory):
    courses = course_factory(_quantity=10)
    list_of_courses = [model_to_dict(course) for course in courses]
    _object = list_of_courses[0]
    id = _object['id']
    response = client.get(f'/courses/?id={id}', content_type='application/json')
    data = response.json()
    assert response.status_code == 200
    assert data == [_object]

@pytest.mark.django_db
def test_courses_name(client, course_factory):
    courses = course_factory(_quantity=10)
    list_of_courses = [model_to_dict(course) for course in courses]
    _object = list_of_courses[0]
    name = _object['name']
    response = client.get(f'/courses/?name={name}', content_type='application/json')
    data = response.json()
    assert response.status_code == 200
    assert data == [_object]

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/courses/', data={'name':'python-course'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    id = courses[0].id
    response = client.patch(f'/courses/{id}/', data={'name': 'java-course'}, follow=True)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    id = courses[0].id
    response = client.delete(f'/courses/{id}/')
    assert response.status_code == 204


