from behave import given, when, then
from tribunal import liberar_entrada_sala_de_provas, preparar, CICLOS_DE_DETECCAO_DE_SAIDA
import simpy


@given('advogados/promotores estão próximos da sala de provas')
def step_given_advogados_promotores_proximos_sala_provas(context):
    context.advogados_promotores_reconhecidos = {
        "1": {"nome": "Advogado 1", "codigo": "1", "em_tribunal": False, "em_sala_de_provas": False},
        "2": {"nome": "Advogado 2", "codigo": "2", "em_tribunal": False, "em_sala_de_provas": False}
    }
    context.ambiente = simpy.Environment()
    assert any(not advogado_promotor["em_sala_de_provas"]
               for advogado_promotor in context.advogados_promotores_reconhecidos.values())


@when('o sistema permite a entrada na sala de provas')
def step_when_sistema_permite_entrada_sala_provas(context):
    evento = liberar_entrada_sala_de_provas(
        context.ambiente, context.advogados_promotores_reconhecidos)
    context.ambiente.process(evento)
    # Avançar o ambiente de simulação para permitir a execução do evento
    context.ambiente.run(until=CICLOS_DE_DETECCAO_DE_SAIDA * 10)


@then('advogados/promotores devem ser permitidos a entrar na sala de provas com base na probabilidade')
def step_then_advogados_promotores_permitidos_entrada(context):
    permitidos = any(advogado_promotor["em_sala_de_provas"]
                     for advogado_promotor in context.advogados_promotores_reconhecidos.values())
    assert permitidos
