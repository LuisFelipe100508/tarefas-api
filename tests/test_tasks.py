import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tasks.models import Task


def test_rota_exige_autenticacao():
    resp = APIClient().get(reverse("task-list"))
    assert resp.status_code == 401


def test_criar_tarefa_define_dono_automaticamente(client_ana, ana):
    resp = client_ana.post(reverse("task-list"), {"title": "Estudar"})
    assert resp.status_code == 201
    assert Task.objects.get(id=resp.data["id"]).owner == ana


def test_cliente_nao_consegue_definir_dono(client_ana, ana, bob):
    resp = client_ana.post(
        reverse("task-list"), {"title": "Tentativa", "owner": bob.id}
    )
    assert resp.status_code == 201
    assert Task.objects.get(id=resp.data["id"]).owner == ana


def test_listagem_mostra_apenas_tarefas_do_usuario(client_ana, client_bob, ana, bob):
    Task.objects.create(owner=ana, title="da ana")
    Task.objects.create(owner=bob, title="do bob")

    resp = client_ana.get(reverse("task-list"))

    assert resp.status_code == 200
    assert resp.data["count"] == 1
    assert resp.data["results"][0]["title"] == "da ana"


def test_outro_usuario_recebe_404_ao_acessar_tarefa_alheia(client_bob, ana):
    tarefa = Task.objects.create(owner=ana, title="privada")
    resp = client_bob.get(reverse("task-detail", args=[tarefa.id]))
    assert resp.status_code == 404


def test_outro_usuario_nao_edita_nem_apaga_tarefa_alheia(client_bob, ana):
    tarefa = Task.objects.create(owner=ana, title="privada")
    url = reverse("task-detail", args=[tarefa.id])

    assert client_bob.patch(url, {"title": "hackeada"}).status_code == 404
    assert client_bob.delete(url).status_code == 404

    tarefa.refresh_from_db()
    assert tarefa.title == "privada"


def test_dono_edita_e_apaga_a_propria_tarefa(client_ana, ana):
    tarefa = Task.objects.create(owner=ana, title="minha")
    url = reverse("task-detail", args=[tarefa.id])

    assert client_ana.patch(url, {"status": "done"}).status_code == 200
    assert client_ana.delete(url).status_code == 204