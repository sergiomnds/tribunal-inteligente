from behave import given, when, then
from tribunal import liberar_tribunal, preparar, CICLOS_DE_DETECCAO_DE_LIBERACAO_DE_SALAS
import simpy


@given('advogados/promotores estão em tribunal')
def step_given_advogados_promotores_em_tribunal(context):
    context.advogados_promotores_reconhecidos = {
        "1": {"nome": "Advogado 1", "codigo": "1", "em_tribunal": True, "em_sala_de_provas": False},
        "2": {"nome": "Advogado 2", "codigo": "2", "em_tribunal": True, "em_sala_de_provas": False}
    }
    context.ambiente = simpy.Environment()
    assert any(advogado_promotor["em_tribunal"]
               for advogado_promotor in context.advogados_promotores_reconhecidos.values())


@when('o sistema libera o tribunal')
def step_when_sistema_libera_tribunal(context):
    evento = liberar_tribunal(
        context.ambiente, context.advogados_promotores_reconhecidos)
    context.ambiente.process(evento)
    # Avançar o ambiente de simulação para permitir a execução do evento
    context.ambiente.run(until=CICLOS_DE_DETECCAO_DE_LIBERACAO_DE_SALAS * 10)


@then('advogados/promotores devem ser liberados do tribunal com base na probabilidade')
def step_then_advogados_promotores_liberados(context):
    liberados = any(not advogado_promotor["em_tribunal"]
                    for advogado_promotor in context.advogados_promotores_reconhecidos.values())
    assert liberados
