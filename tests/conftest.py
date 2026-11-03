import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

PASSWORD = "SenhaForte#2026x"


@pytest.fixture(autouse=True)
def limpar_cache():
    # O throttling usa o cache; sem limpar, os testes se bloqueiam entre si
    cache.clear()


@pytest.fixture
def ana(db, django_user_model):
    return django_user_model.objects.create_user(username="ana", password=PASSWORD)


@pytest.fixture
def bob(db, django_user_model):
    return django_user_model.objects.create_user(username="bob", password=PASSWORD)


@pytest.fixture
def client_ana(ana):
    client = APIClient()
    client.force_authenticate(user=ana)
    return client


@pytest.fixture
def client_bob(bob):
    client = APIClient()
    client.force_authenticate(user=bob)
    return client