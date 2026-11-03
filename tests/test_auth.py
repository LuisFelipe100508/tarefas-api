import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .conftest import PASSWORD


@pytest.mark.django_db
def test_registro_cria_usuario_sem_expor_senha():
    resp = APIClient().post(
        reverse("register"),
        {"username": "carla", "email": "c@x.com", "password": PASSWORD},
    )
    assert resp.status_code == 201
    assert "password" not in resp.data


@pytest.mark.django_db
def test_registro_recusa_senha_fraca():
    resp = APIClient().post(
        reverse("register"), {"username": "carla", "password": "12345678"}
    )
    assert resp.status_code == 400


def test_login_retorna_tokens(ana):
    resp = APIClient().post(
        reverse("token_obtain"), {"username": "ana", "password": PASSWORD}
    )
    assert resp.status_code == 200
    assert "access" in resp.data and "refresh" in resp.data


def test_login_com_senha_errada_retorna_401(ana):
    resp = APIClient().post(
        reverse("token_obtain"), {"username": "ana", "password": "errada"}
    )
    assert resp.status_code == 401