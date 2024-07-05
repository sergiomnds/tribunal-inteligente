Feature: Liberar Tribunal

  Scenario: Liberar advogados/promotores do tribunal com base na probabilidade
    Given advogados/promotores estão em tribunal
    When o sistema libera o tribunal
    Then advogados/promotores devem ser liberados do tribunal com base na probabilidade
