Feature: Reconhecimento de Participantes

  Scenario: Reconhecer advogados, promotores e réus entre os participantes
    Given o ambiente está inicializado
    And a configuração está carregada
    And não há advogados/promotores reconhecidos
    And não há réus reconhecidos
    When o sistema reconhece participantes
    Then advogados/promotores devem ser reconhecidos se estiverem presentes
    And réus devem ser reconhecidos se estiverem presentes
