Feature: Preparar o Sistema

  Scenario: Carregar configuração e preparar o ambiente
    Given o arquivo de configuração está disponível
    When o sistema é preparado
    Then o sistema deve estar preparado com sucesso
    And o ambiente deve ser inicializado
    And a configuração deve ser carregada
