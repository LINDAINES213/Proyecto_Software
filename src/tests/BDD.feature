Feature: Gestión de circulares para estudiantes

Scenario: Enviar una circular para estudiantes
    Given que estoy autenticado como secretario
    When lleno los campos de título y contenido de la circular
    Then debería ser redirigido a la página de ver circulares