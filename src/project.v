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

 /** No modifiques la definición del módulo, sólo el nombre. 
  * El módulo principal de tu diseño debe partir con "tt_um_" y debe tener exactamente
  * la misma interfaz que el módulo de ejemplo.
  * */
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
  /* A partir de aquí puedes borrar el código actual e implementar tu lógica */
  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
