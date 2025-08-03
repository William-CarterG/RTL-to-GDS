## NOTAS PARA PERSONALIZACIÓN DE TU DISEÑO

### INSTRUCCIONES PARA ADAPTAR ESTE MÓDULO A TU PROYECTO:

1. **CAMBIAR EL NOMBRE DEL MÓDULO:**
   - Reemplaza "tt_um_project_example" con un nombre descriptivo
   - El nombre del módulo principal debe partir con "tt_um_" por ser parte del flujo de Tiny Tapeout
   - Actualiza también tb.v para usar el nuevo nombre

2. **IMPLEMENTAR TU LÓGICA:**
   - Reemplaza la línea "assign uo_out = ui_in + uio_in;" 
   - Implementa tu funcionalidad específica (FSM, ALU, etc.)

3. **USAR SEÑALES DE RELOJ Y RESET (SI NECESITAS LÓGICA SECUENCIAL):**
   ```verilog
   always_ff @(posedge clk or negedge rst_n) begin
       if (!rst_n) begin
           // Estado de reset
       end else if (ena) begin
           // Lógica normal
       end
   end
   ```

4. **CONFIGURAR PINES BIDIRECCIONALES (SI LOS NECESITAS):**
   ```verilog
   // Para usar uio[3:0] como salidas y uio[7:4] como entradas:
   assign uio_oe = 8'b0000_1111;  // Bits 3:0 como salidas
   assign uio_out[3:0] = tu_salida;
   wire [3:0] tu_entrada = uio_in[7:4];
   ```

5. **OPTIMIZACIÓN PARA ÁREA/VELOCIDAD:**
   - Usa registros solo cuando sea necesario
   - Minimiza la lógica combinacional compleja
   - Considera el pipeline para diseños de alta velocidad

### EJEMPLOS DE DISEÑOS TÍPICOS:

#### A) CPU Simple de 8-bits:
- ui_in: datos de entrada o código de operación
- uo_out: resultado de ALU o datos de salida
- uio: bus de direcciones o datos adicionales

#### B) Controlador de Periférico:
- ui_in: comandos de configuración
- uo_out: estado o datos leídos
- uio: interfaz con periférico externo (I2C, SPI, etc.)

#### C) Procesador de Señales:
- ui_in: muestras de entrada
- uo_out: muestras procesadas
- uio: parámetros de configuración

### RECURSOS ÚTILES:
- [Tiny Tapeout HDL Guide](https://tinytapeout.com/hdl/)
- [Verilog Reference](https://www.verilog.com/)
- [SkyWater PDK](https://skywater-pdk.readthedocs.io/)