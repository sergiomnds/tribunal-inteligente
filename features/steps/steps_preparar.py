from behave import given, when, then
import os
from tribunal import preparar


@given('o arquivo de configuração está disponível')
def step_given_arquivo_configuracao_disponivel(context):
    context.config_path = 'configuracao.json'
    assert os.path.exists(context.config_path) is True


@when('o sistema é preparado')
def step_when_sistema_preparado(context):
    context.preparado, context.ambiente, context.configuracao = preparar()


@then('o sistema deve estar preparado com sucesso')
def step_then_sistema_preparado_com_sucesso(context):
    assert context.preparado is True


@then('o ambiente deve ser inicializado')
def step_then_ambiente_inicializado(context):
    assert context.ambiente is not None


@then('a configuração deve ser carregada')
def step_then_configuracao_carregada(context):
    assert context.configuracao is not None
    assert isinstance(context.configuracao, dict)
