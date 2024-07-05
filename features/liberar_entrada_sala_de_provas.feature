Feature: Liberar Entrada na Sala de Provas

  Scenario: Permitir a entrada de advogados/promotores na sala de provas
    Given advogados/promotores estão próximos da sala de provas
    When o sistema permite a entrada na sala de provas
    Then advogados/promotores devem ser permitidos a entrar na sala de provas com base na probabilidade
