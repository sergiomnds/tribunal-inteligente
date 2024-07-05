# steps_reservar_tribunal.py
from behave import given, when, then
from tribunal import TOTAL_DE_SALAS_DE_TRIBUNAL, reservar_tribunal, preparar, CICLOS_DE_DETECCAO_DE_RESERVA_DE_SALAS
import simpy


@given('advogados/promotores estão disponíveis')
def step_given_advogados_promotores_disponiveis(context):
    context.advogados_promotores_reconhecidos = {
        "1": {"nome": "Advogado 1", "codigo": "1", "em_tribunal": False, "em_sala_de_provas": False},
        "2": {"nome": "Advogado 2", "codigo": "2", "em_tribunal": False, "em_sala_de_provas": False}
    }
    assert len(context.advogados_promotores_reconhecidos) > 0


@when('o sistema reserva o tribunal')
def step_when_sistema_reserva_tribunal(context):
    evento = reservar_tribunal(
        context.ambiente, context.advogados_promotores_reconhecidos)
    context.ambiente.process(evento)
    # Avançar o ambiente de simulação para permitir a execução do evento
    context.ambiente.run(until=CICLOS_DE_DETECCAO_DE_RESERVA_DE_SALAS * 10)


@then('advogados/promotores devem ser reservados para tribunal com base na probabilidade')
def step_then_advogados_promotores_reservados(context):
    reservados = any(advogado_promotor["em_tribunal"]
                     for advogado_promotor in context.advogados_promotores_reconhecidos.values())
    assert reservados


@then('a capacidade do tribunal não deve ser excedida')
def step_then_capacidade_tribunal_nao_excedida(context):
    total_em_tribunal = sum(1 for advogado_promotor in context.advogados_promotores_reconhecidos.values(
    ) if advogado_promotor["em_tribunal"])
    assert total_em_tribunal <= TOTAL_DE_SALAS_DE_TRIBUNAL
