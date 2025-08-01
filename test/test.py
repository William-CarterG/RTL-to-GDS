# SPDX-FileCopyrightText: 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

"""
Testbench para Proyecto RTL-to-GDS
==================================

Este testbench utiliza cocotb (COroutine COsimulation TestBench) para verificar
el funcionamiento de tu diseño RTL antes de proceder con el flujo RTL-to-GDS.

cocotb permite escribir testbenches en Python, ofreciendo mayor flexibilidad
y facilidad de uso comparado con testbenches tradicionales en Verilog/SystemVerilog.

Autor: Basado en templates de Tiny Tapeout
Documentación adicional: https://docs.cocotb.org/
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    """
    Test principal del diseño RTL
    
    Este test verifica el comportamiento básico del módulo bajo test (DUT).
    Modifica esta función según la funcionalidad específica de tu diseño.
    
    Args:
        dut: Device Under Test - referencia al módulo que se está probando
    """
    dut._log.info("=== Iniciando Test del Proyecto ===")

    # ========================================================================
    # CONFIGURACIÓN DEL RELOJ
    # ========================================================================
    # Configurar el reloj del sistema a 100 KHz (período de 10 µs)
    # Ajusta la frecuencia según las necesidades de tu diseño
    clock_period_us = 10
    clock_freq_khz = 1000 / clock_period_us
    
    dut._log.info(f"Configurando reloj a {clock_freq_khz} KHz (período: {clock_period_us} µs)")
    clock = Clock(dut.clk, clock_period_us, units="us")
    cocotb.start_soon(clock.start())

    # ========================================================================
    # SECUENCIA DE RESET
    # ========================================================================
    dut._log.info("Ejecutando secuencia de reset...")
    
    # Configurar señales de control
    dut.ena.value = 1      # Habilitar el diseño (siempre 1 en Tiny Tapeout)
    dut.ui_in.value = 0    # Limpiar entradas dedicadas
    dut.uio_in.value = 0   # Limpiar entradas bidireccionales
    
    # Aplicar reset (activo bajo)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)  # Mantener reset por 10 ciclos
    
    # Liberar reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)   # Esperar estabilización
    
    dut._log.info("Reset completado")

    # ========================================================================
    # PRUEBAS DE FUNCIONALIDAD
    # ========================================================================
    dut._log.info("=== Iniciando Pruebas de Funcionalidad ===")

    # Test Case 1: Valores básicos de entrada
    dut._log.info("Test Case 1: Verificando suma básica")
    
    # Configurar valores de entrada para probar
    input_a = 20  # Valor para ui_in
    input_b = 30  # Valor para uio_in
    expected_output = input_a + input_b  # Resultado esperado según la lógica del ejemplo
    
    # Aplicar estímulos
    dut.ui_in.value = input_a
    dut.uio_in.value = input_b
    
    # Esperar un ciclo de reloj para que se propague el resultado
    await ClockCycles(dut.clk, 1)
    
    # Verificar resultado
    actual_output = int(dut.uo_out.value)
    dut._log.info(f"Entrada A: {input_a}, Entrada B: {input_b}")
    dut._log.info(f"Salida esperada: {expected_output}, Salida actual: {actual_output}")
    
    # Assertion para verificar correctitud
    # IMPORTANTE: Modifica esta verificación según tu lógica específica
    assert actual_output == expected_output, \
        f"Error: esperado {expected_output}, obtenido {actual_output}"
    
    dut._log.info("✓ Test Case 1: PASADO")

    # ========================================================================
    # CASOS DE PRUEBA ADICIONALES
    # ========================================================================
    # Agrega aquí más casos de prueba según tu diseño específico
    
    # Test Case 2: Casos límite
    dut._log.info("Test Case 2: Verificando casos límite")
    
    test_cases = [
        (0, 0),      # Valores mínimos
        (255, 255),  # Valores máximos (8 bits)
        (128, 127),  # Valores medios
        (1, 254),    # Casos especiales
    ]
    
    for i, (val_a, val_b) in enumerate(test_cases):
        dut.ui_in.value = val_a
        dut.uio_in.value = val_b
        await ClockCycles(dut.clk, 1)
        
        expected = val_a + val_b
        actual = int(dut.uo_out.value)
        
        # Para sumas que excedan 8 bits, considerar overflow
        if expected > 255:
            expected = expected & 0xFF  # Mantener solo los 8 bits menos significativos
            
        dut._log.info(f"Test {i+1}: {val_a} + {val_b} = {actual} (esperado: {expected})")
        
        assert actual == expected, \
            f"Test Case {i+1} falló: esperado {expected}, obtenido {actual}"
    
    dut._log.info("✓ Test Case 2: PASADO")

    # ========================================================================
    # TEST DE RESET DURANTE OPERACIÓN
    # ========================================================================
    dut._log.info("Test Case 3: Verificando comportamiento durante reset")
    
    # Configurar una entrada
    dut.ui_in.value = 100
    dut.uio_in.value = 50
    await ClockCycles(dut.clk, 1)
    
    # Aplicar reset durante operación
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    
    # Verificar que las salidas se comporten apropiadamente durante reset
    # (esto depende de tu implementación específica)
    dut._log.info(f"Salida durante reset: {int(dut.uo_out.value)}")
    
    # Liberar reset y verificar funcionamiento normal
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
    
    expected_after_reset = 100 + 50
    actual_after_reset = int(dut.uo_out.value)
    
    assert actual_after_reset == expected_after_reset, \
        f"Falló recuperación post-reset: esperado {expected_after_reset}, obtenido {actual_after_reset}"
    
    dut._log.info("✓ Test Case 3: PASADO")

    # ========================================================================
    # FINALIZACIÓN
    # ========================================================================
    dut._log.info("=== Todas las Pruebas Completadas Exitosamente ===")
    dut._log.info("El diseño está listo para el flujo RTL-to-GDS")


# ============================================================================
# FUNCIONES DE UTILIDAD (OPCIONAL)
# ============================================================================

async def setup_dut(dut, clock_period_us=10):
    """
    Función de utilidad para configuración inicial del DUT
    
    Args:
        dut: Device Under Test
        clock_period_us: Período del reloj en microsegundos
    """
    # Inicializar reloj
    clock = Clock(dut.clk, clock_period_us, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset inicial
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)


async def apply_test_vector(dut, ui_in_val, uio_in_val, expected_out=None):
    """
    Función de utilidad para aplicar un vector de test
    
    Args:
        dut: Device Under Test
        ui_in_val: Valor para entrada dedicada
        uio_in_val: Valor para entrada bidireccional
        expected_out: Valor esperado de salida (opcional)
    
    Returns:
        int: Valor actual de salida
    """
    dut.ui_in.value = ui_in_val
    dut.uio_in.value = uio_in_val
    await ClockCycles(dut.clk, 1)
    
    actual_out = int(dut.uo_out.value)
    
    if expected_out is not None:
        assert actual_out == expected_out, \
            f"Vector de test falló: esperado {expected_out}, obtenido {actual_out}"
    
    return actual_out


# ============================================================================
# NOTAS PARA PERSONALIZACIÓN
# ============================================================================
"""
INSTRUCCIONES PARA ADAPTAR ESTE TESTBENCH A TU DISEÑO:

1. MODIFICA LA LÓGICA DE VERIFICACIÓN:
   - Cambia las assertions según tu funcionalidad específica
   - El ejemplo actual asume que uo_out = ui_in + uio_in

2. AGREGA TESTS ESPECÍFICOS:
   - Crea funciones de test adicionales con @cocotb.test()
   - Prueba todas las funcionalidades de tu módulo
   
3. AJUSTA LOS PARÁMETROS DE RELOJ:
   - Modifica clock_period_us según tu diseño
   - Considera las restricciones de timing de tu lógica

4. VERIFICA SEÑALES BIDIRECCIONALES:
   - Si usas uio_out y uio_oe, agrega verificaciones apropiadas
   - Prueba diferentes configuraciones de entrada/salida

5. AGREGA MONITOREO DE SEÑALES INTERNAS:
   - Usa dut.signal_name para acceder a señales internas
   - Útil para debugging de lógica compleja

RECURSOS ADICIONALES:
- Documentación cocotb: https://docs.cocotb.org/
- Ejemplos de Tiny Tapeout: https://tinytapeout.com/hdl/testing/
- Referencia de triggers: https://docs.cocotb.org/en/stable/triggers.html