Feature: Liberação de Réus

  Scenario: Liberar réus do julgamento
    Given o ambiente está inicializado
    And a configuração está carregada
    And réus estão em julgamento
    When o sistema libera réus
    Then réus devem ser liberados com base na probabilidade
