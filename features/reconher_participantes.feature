Feature: Reconhecimento de Participantes
  Scenario: Reconhecer advogados, promotores e réus
    Given o sistema está preparado
    When o sistema começa a reconhecer participantes
    Then o sistema deve reconhecer advogados e promotores
    And o sistema deve reconhecer réus
