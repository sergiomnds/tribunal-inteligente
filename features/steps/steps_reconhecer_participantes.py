from behave import given, when, then
from tribunal import preparar, reconhecer_participantes
import simpy


@given('o sistema está preparado')
def step_given_sistema_preparado(context):
    context.preparado, context.ambiente, context.configuracao = preparar()
    assert context.preparado is True


@when('o sistema começa a reconhecer participantes')
def step_when_reconhecer_participantes(context):
    context.advogados_promotores_reconhecidos = {}
    context.reus_reconhecidos = {}
    context.ambiente.process(reconhecer_participantes(
        context.ambiente, context.configuracao, context.advogados_promotores_reconhecidos, context.reus_reconhecidos))
    context.ambiente.run(until=40)


@then('o sistema deve reconhecer advogados e promotores')
def step_then_reconhecer_advogados_promotores(context):
    assert len(context.advogados_promotores_reconhecidos) > 0


@then('o sistema deve reconhecer réus')
def step_then_reconhecer_reus(context):
    assert len(context.reus_reconhecidos) > 0
