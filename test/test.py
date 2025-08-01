# SPDX-FileCopyrightText: 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# =============================================================================
# Plantilla de Prueba RTL-to-GDS
# =============================================================================
# INSTRUCCIONES:
# 1. Esta es una plantilla mínima funcional para tu proyecto RTL-to-GDS
# 2. Las secciones marcadas con comentarios "TODO" indican dónde debes agregar tu propio código
# 3. Mantén la función safe_get_int ya que maneja valores 'X' en la simulación
# 4. Agrega casos de prueba específicos basados en la funcionalidad de tu diseño
# =============================================================================

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_basic_functionality(dut):
    """Prueba de funcionalidad básica del diseño"""
    dut._log.info("=== Probando Funcionalidad Básica ===")
    
    # Configurar reloj - período de 10us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Inicializar entradas
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    # Aplicar reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    
    # Esperar algunos ciclos de reloj y verificar salidas
    await ClockCycles(dut.clk, 10)
    
    # Registrar los valores de salida
    dut._log.info(f"Valor de uo_out: {dut.uo_out.value}")

    # Prueba simple - solo verifica que se puedan leer las salidas sin errores
    dut._log.info("Prueba básica completada exitosamente")