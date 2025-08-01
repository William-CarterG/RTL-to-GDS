/*
 * SPDX-License-Identifier: Apache-2.0
 * 
 * Proyecto RTL-to-GDS - Módulo de Ejemplo
 * =======================================
 * 
 * Este archivo contiene un ejemplo de módulo Verilog compatible con la
 * interfaz estándar de Tiny Tapeout. Reemplaza este código con tu diseño
 * específico manteniendo la misma interfaz de señales.
 * 
 * IMPORTANTE: Este es solo un ejemplo. Tu lógica real puedes implementarla sobre otro archivo en este directorio. Tan sólo recuerda ajustar el Makefile para que apunte a tu archivo.
 * 
 * Documentación de Tiny Tapeout: https://tinytapeout.com
 * 
 * Autor: Basado en templates de Tiny Tapeout
 * Fecha: 2024
 */

`default_nettype none

/**
 * Módulo Principal del Proyecto RTL-to-GDS
 * ========================================
 * 
 * Este módulo implementa la lógica principal de tu diseño y debe seguir
 * la interfaz estándar definida por Tiny Tapeout para garantizar 
 * compatibilidad con el flujo RTL-to-GDS.
 * 
 * La interfaz proporciona:
 * - 8 bits de entrada dedicados (ui_in)
 * - 8 bits de salida dedicados (uo_out) 
 * - 8 bits bidireccionales configurables (uio_in/uio_out/uio_oe)
 * - Señales de control estándar (clk, rst_n, ena)
 */
module tt_um_project_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule

// ========================================================================
// NOTAS PARA PERSONALIZACIÓN DE TU DISEÑO
// ========================================================================

/*
 * INSTRUCCIONES PARA ADAPTAR ESTE MÓDULO A TU PROYECTO:
 * 
 * 1. CAMBIAR EL NOMBRE DEL MÓDULO:
 *    - Reemplaza "tt_um_project_example" con un nombre descriptivo
 *    - El nombre del módulo principal debe partir con "tt_um_" por ser parte del flujo de Tiny Tapeout
 *    - Actualiza también tb.v para usar el nuevo nombre
 * 
 * 2. IMPLEMENTAR TU LÓGICA:
 *    - Reemplaza la línea "assign uo_out = ui_in + uio_in;" 
 *    - Implementa tu funcionalidad específica (FSM, ALU, etc.)
 * 
 * 3. USAR SEÑALES DE RELOJ Y RESET (SI NECESITAS LÓGICA SECUENCIAL):
 *    always_ff @(posedge clk or negedge rst_n) begin
 *        if (!rst_n) begin
 *            // Estado de reset
 *        end else if (ena) begin
 *            // Lógica normal
 *        end
 *    end
 * 
 * 4. CONFIGURAR PINES BIDIRECCIONALES (SI LOS NECESITAS):
 *    // Para usar uio[3:0] como salidas y uio[7:4] como entradas:
 *    assign uio_oe = 8'b0000_1111;  // Bits 3:0 como salidas
 *    assign uio_out[3:0] = tu_salida;
 *    wire [3:0] tu_entrada = uio_in[7:4];
 * 
 * 5. OPTIMIZACIÓN PARA ÁREA/VELOCIDAD:
 *    - Usa registros solo cuando sea necesario
 *    - Minimiza la lógica combinacional compleja
 *    - Considera el pipeline para diseños de alta velocidad
 * 
 * EJEMPLOS DE DISEÑOS TÍPICOS:
 * 
 * A) CPU Simple de 8-bits:
 *    - ui_in: datos de entrada o código de operación
 *    - uo_out: resultado de ALU o datos de salida
 *    - uio: bus de direcciones o datos adicionales
 * 
 * B) Controlador de Periférico:
 *    - ui_in: comandos de configuración
 *    - uo_out: estado o datos leídos
 *    - uio: interfaz con periférico externo (I2C, SPI, etc.)
 * 
 * C) Procesador de Señales:
 *    - ui_in: muestras de entrada
 *    - uo_out: muestras procesadas
 *    - uio: parámetros de configuración
 * 
 * RECURSOS ÚTILES:
 * - Tiny Tapeout HDL Guide: https://tinytapeout.com/hdl/
 * - Verilog Reference: https://www.verilog.com/
 * - SkyWater PDK: https://skywater-pdk.readthedocs.io/
 */
