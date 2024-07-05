Feature: Reserva de Tribunal

  Scenario: Reservar tribunal para advogados e promotores
    Given o ambiente está inicializado
    And a configuração está carregada
    And advogados/promotores estão disponíveis
    When o sistema reserva o tribunal
    Then advogados/promotores devem ser reservados para tribunal com base na probabilidade
    And a capacidade do tribunal não deve ser excedida
