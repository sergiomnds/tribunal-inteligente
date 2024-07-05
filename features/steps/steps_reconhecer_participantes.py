# steps_reconhecer_participantes.py
from behave import given, when, then
from tribunal import reconhecer_participantes, preparar
import simpy


@given('o ambiente está inicializado')
def step_given_ambiente_inicializado(context):
    context.preparado, context.ambiente, context.configuracao = preparar()
    assert context.preparado is True
    assert context.ambiente is not None


@given('a configuração está carregada')
def step_given_configuracao_carregada(context):
    assert context.configuracao is not None
    assert isinstance(context.configuracao, dict)


@given('não há advogados/promotores reconhecidos')
def step_given_nao_ha_advogados_promotores_reconhecidos(context):
    context.advogados_promotores_reconhecidos = {}
    assert len(context.advogados_promotores_reconhecidos) == 0


@given('não há réus reconhecidos')
def step_given_nao_ha_reus_reconhecidos(context):
    context.reus_reconhecidos = {}
    assert len(context.reus_reconhecidos) == 0


@when('o sistema reconhece participantes')
def step_when_sistema_reconhece_participantes(context):
    evento = reconhecer_participantes(context.ambiente, context.configuracao,
                                      context.advogados_promotores_reconhecidos, context.reus_reconhecidos)
    next(evento)


@then('advogados/promotores devem ser reconhecidos se estiverem presentes')
def step_then_advogados_promotores_reconhecidos(context):
    if context.configuracao['advogadosPromotores']:
        assert len(context.advogados_promotores_reconhecidos) > 0


@then('réus devem ser reconhecidos se estiverem presentes')
def step_then_reus_reconhecidos(context):
    if context.configuracao['reus']:
        assert len(context.reus_reconhecidos) > 0
