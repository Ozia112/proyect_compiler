# 🗿 Compilador del Lenguaje Tan

> Un compilador educativo para el lenguaje de programación "Tan", basado en el sistema de numeración maya.

## 📋 Descripción

Este proyecto implementa un compilador completo para el lenguaje de programación "Tan", desarrollado como proyecto integrador para la materia de **Teoría de la Computación** en la Universidad Autónoma de Yucatán. El lenguaje utiliza el sistema de numeración maya (base 20) y está inspirado en el lenguaje MiniLang visto en clase.

## 🌟 Características

- **Sistema de numeración maya**: Utiliza puntos (.), barras (|) y ceros (0) para representar números
- **Análisis léxico**: Tokenización completa del código fuente
- **Análisis sintáctico**: Parser recursivo descendente
- **Generación de código**: Traduce a Python ejecutable
- **Manejo de errores**: Detección y reporte de errores léxicos y sintácticos

## 🔢 Sistema de Numeración Maya

El lenguaje Tan utiliza el sistema vigesimal (base 20) maya:

| Símbolo | Valor | Ejemplo | Decimal |
|---------|-------|---------|---------|
| `.` | 1 | `...` | 3 |
| `\|` | 5 | `\|\|` | 10 |
| `0` | 0 | `0` | 0 |
| `,` | Separador de posiciones | `., .` | 21 |

### Ejemplos de números:
- `..||` = 12 (2 puntos + 2 barras = 2 + 10)
- `0 , .` = 20 (0×20¹ + 1×20⁰)
- `..|, ..` = 47 (7×20⁰ + 2×20¹)
- `0 , 0 , 0 , 0 , .` = 160,000

## 📖 Sintaxis del Lenguaje

### Palabras Reservadas

| Palabra | Significado | Equivalente |
|---------|-------------|-------------|
| `xiib` | Declaración de variable | `let` |
| `tsiibil` | Imprimir en pantalla | `print` |
| `keet` | Operador de asignación | `=` |

### Operadores

- `+` : Suma
- `-` : Resta
- `*` : Multiplicación
- `/` : División
- `[` `]` : Paréntesis (agrupación)

### Gramática BNF

```bnf
<program>    ::= <statement> { <statement> }

<statement>  ::= "xiib" <identifier> "keet" <expression>
             |   "tsiibil" "[" <expression> "]"

<expression> ::= <term> { ("+" | "-") <term> }

<term>       ::= <factor> { ("*" | "/") <factor> }

<factor>     ::= NUMBER | IDENT | "[" <expression> "]"
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.8 o superior
- No requiere dependencias externas

### Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/compilador-tan.git
cd compilador-tan
```

2. Asegúrate de tener Python instalado:
```bash
python --version
```

### Uso Básico

1. Ejecuta el compilador con los casos de prueba incluidos:
```bash
python tan_compiler.py
```

2. Para compilar tu propio código Tan:
```python
from tan_compiler import compile_tan

codigo = """
xiib x keet |
xiib y keet ..||
tsiibil [x + y]
"""

# Compilar y ejecutar
codigo_python = compile_tan(codigo)
if codigo_python:
    exec(codigo_python)
```

## 💡 Ejemplos

### Ejemplo 1: Hola Mundo en Tan
```tan
xiib saludo keet . , |
tsiibil [saludo]
```
Output: `25`

### Ejemplo 2: Operaciones Aritméticas
```tan
xiib a keet ..||
xiib b keet |
xiib resultado keet a + b * ..
tsiibil [resultado]
```
Output: `22` (12 + 5 × 2)

### Ejemplo 3: Números Grandes
```tan
xiib poblacion keet . , . , . , .
tsiibil [poblacion]
```
Output: `8421` (1×20³ + 1×20² + 1×20¹ + 1×20⁰)

## 🔧 Estructura del Proyecto

```
XD algo pondre luego XDDD
```

## 🧪 Casos de Prueba

El compilador incluye casos de prueba tanto positivos como negativos:

### Casos Positivos ✅
- Declaración de variables
- Operaciones aritméticas
- Impresión de resultados
- Números mayas complejos

### Casos Negativos ❌
- Errores sintácticos (falta de palabras clave)
- Paréntesis sin cerrar
- Caracteres inválidos
- Operaciones mal formadas

## 🏗️ Arquitectura del Compilador

### 1. Análisis Léxico (Lexer)
- Convierte el código fuente en tokens
- Reconoce números mayas y los convierte a decimal
- Identifica palabras reservadas y operadores

### 2. Análisis Sintáctico (Parser)
- Construye el Árbol de Sintaxis Abstracta (AST)
- Valida la estructura del programa
- Implementa un parser recursivo descendente

### 3. Generación de Código
- Traduce el AST a código Python
- Mantiene la semántica del programa original
- Genera código ejecutable


## 👥 Autores

- **Edrei** - *Hizo todo* - 
- **Tu Nombre** - *se durmio* - 
- **Tu Nombre** - *no fue a la clase :C* - 

<p align="center">
  Hecho con ❤️ en Mérida, Yucatán 🇲🇽
</p>