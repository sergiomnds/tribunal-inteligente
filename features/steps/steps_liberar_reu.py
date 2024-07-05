# steps_liberar_reus.py
from behave import given, when, then
from tribunal import PROBABILIDADE_DE_LIBERACAO_REU, liberar_reus
import simpy
import random


@given('réus estão em julgamento')
def step_given_reus_em_julgamento(context):
    context.reus_reconhecidos = {
        "1": {"nome": "Réu 1", "codigo": "1", "em_julgamento": True},
        "2": {"nome": "Réu 2", "codigo": "2", "em_julgamento": True}
    }
    assert len(context.reus_reconhecidos) > 0


@when('o sistema libera réus')
def step_when_sistema_libera_reus(context):
    evento = liberar_reus(context.ambiente, context.reus_reconhecidos)
    next(evento)


@then('réus devem ser liberados com base na probabilidade')
def step_then_reus_liberados(context):
    for reu in context.reus_reconhecidos.values():
        if reu["em_julgamento"]:
            liberar = (random.randint(1, 100) <=
                       PROBABILIDADE_DE_LIBERACAO_REU)
            if liberar:
                reu["em_julgamento"] = False
    assert all(reu["em_julgamento"] == False for reu in context.reus_reconhecidos.values(
    ) if random.randint(1, 100) <= PROBABILIDADE_DE_LIBERACAO_REU)
