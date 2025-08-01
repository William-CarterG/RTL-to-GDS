# Guía de Testing y Simulación

Esta carpeta contiene todas las herramientas necesarias para probar y verificar tu diseño RTL antes de proceder con el flujo RTL-to-GDS. La verificación es un paso crucial que te ayudará a identificar errores en tu lógica antes de la síntesis física.

## Estructura de Archivos

- **`test.py`**: Testbench principal en Python usando cocotb
- **`tb.v`**: Testbench en Verilog (wrapper para cocotb)
- **`Makefile`**: Automatización de las simulaciones
- **`tb.gtkw`**: Configuración para GTKWave (visor de ondas)

## Configuración del Ambiente de Desarrollo

### Creación de Ambiente Virtual Python

Es altamente recomendado usar un ambiente virtual para evitar conflictos de dependencias:

**En Linux/macOS:**
```bash
# Crear el ambiente virtual
python3 -m venv venv_rtl

# Activar el ambiente virtual
source venv_rtl/bin/activate

# Actualizar pip
pip install --upgrade pip
```

**En Windows:**
```cmd
# Crear el ambiente virtual
python -m venv venv_rtl

# Activar el ambiente virtual
venv_rtl\Scripts\activate

# Actualizar pip
pip install --upgrade pip
```

### Instalación de Dependencias

Una vez activado el ambiente virtual, instala las dependencias necesarias:

**Nota**: Si tu proyecto tiene un archivo `requirements.txt`, simplemente ejecuta:
```bash
pip install -r ./test/requirements.txt
```

## Configuración Inicial

Antes de ejecutar las simulaciones, necesitas configurar algunos archivos:

### 1. Configurar el Makefile

Edita el archivo `Makefile` y asegúrate de que:

- `PROJECT_SOURCES` apunte a tus archivos Verilog fuente
- `MODULE` coincida con el nombre de tu módulo principal
- Las rutas de inclusión sean correctas

Ejemplo de configuración:
```makefile
# Nombre de tu módulo (debe coincidir con el módulo en project.v)
MODULE = tt_um_project_example

# Archivos fuente de tu proyecto
PROJECT_SOURCES = ../src/project.v

# Testbench
TESTBENCH = tb
TOPLEVEL_LANG = verilog
```

### 2. Actualizar tb.v

Modifica `tb.v` para que el nombre del módulo coincida con tu diseño:

```verilog
// Cambiar 'tt_um_project_example' por el nombre de tu módulo
tt_um_project_example version1 (
    // ... conexiones ...
);
```

## Ejecutar Simulaciones

### Simulación RTL (Recomendado para desarrollo)

Para ejecutar la simulación a nivel RTL de tu código Verilog:

```bash
# Asegúrate de estar en el directorio test/
cd test

# Ejecutar simulación RTL
make -B

# O alternativamente:
make clean && make
```

### Simulación Gate-Level (Para verificación final)

Para ejecutar simulación a nivel de compuertas (requiere haber ejecutado primero el flujo RTL-to-GDS):

```bash
# Primero, copia el netlist generado por OpenLane
cp ../runs/wokwi/results/final/verilog/gl/tu_modulo.v gate_level_netlist.v

# Ejecutar simulación gate-level
make -B GATES=yes
```


## Estructura del Testbench

### Testbench en Python (test.py)

El testbench principal está escrito en Python usando cocotb:

```python
@cocotb.test()
async def test_project(dut):
    # Configuración del reloj
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Secuencia de reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    # Tu código de test aquí...
```

**Ventajas de cocotb:**
- Sintaxis Python familiar
- Capacidades avanzadas de verificación
- Generación automática de estímulos
- Fácil integración con librerías de análisis

### Mejores Prácticas para Testing

1. **Test Incremental**: Comienza con casos simples y aumenta la complejidad
2. **Cobertura Completa**: Asegúrate de probar todos los paths de tu código
3. **Casos Edge**: Prueba condiciones límite y casos especiales
4. **Documentación**: Comenta claramente qué está probando cada test

#### Ejemplo de Test Estructurado:

```python
@cocotb.test()
async def test_basic_functionality(dut):
    """Test básico de funcionalidad principal"""
    # Setup inicial
    await setup_dut(dut)
    
    # Test case 1: Operación normal
    await test_normal_operation(dut)
    
    # Test case 2: Condiciones de reset
    await test_reset_conditions(dut)
    
    # Test case 3: Casos límite
    await test_edge_cases(dut)
```

## Debugging y Troubleshooting

### Errores Comunes:

1. **Módulo no encontrado**: Verifica que `MODULE` en Makefile coincida con tu módulo
2. **Archivos fuente no encontrados**: Revisa las rutas en `PROJECT_SOURCES`

### Técnicas de Debug:

```python
# Logging detallado
dut._log.info(f"Valor de entrada: {dut.ui_in.value}")

# Assertions para verificar condiciones
assert dut.uo_out.value == expected_value, f"Esperado {expected_value}, obtenido {dut.uo_out.value}"

# Esperas condicionales
await RisingEdge(dut.signal_ready)  # Esperar hasta que una señal esté lista
```

### Logs Importantes:

- **Salida de la simulación**: Revisa la terminal para mensajes de error
- **Logs de cocotb**: Información detallada sobre la ejecución del test

## Integración Continua

Para automatizar tus tests, puedes usar GitHub Actions. El repositorio incluye workflows que ejecutan automáticamente tus tests en cada push.

## Comandos Útiles

```bash
# Limpiar archivos temporales
make clean

# Ejecutar test específico
make MODULE=test.py::test_specific_function

# Ver ayuda del Makefile
make help

# Ejecutar con logs detallados
make COCOTB_LOG_LEVEL=DEBUG

# Generar coverage report (si está configurado)
make coverage
```

## Siguiente Paso: RTL-to-GDS

Una vez que tus tests pasen satisfactoriamente, estarás listo para ejecutar el flujo RTL-to-GDS:

```bash
cd ..  # Volver al directorio raíz
make harden  # Ejecutar flujo completo
```

Además, recuerda que con cada push a tu repositorio remoto, se ejecutarán el flujo completo automáticamente.

---

**¿Problemas con el testing?** Revisa que tu ambiente virtual esté activado y que todas las dependencias estén instaladas correctamente.
