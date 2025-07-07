# Proyecto Integrador - Teoría de la Computación

## Universidad Autónoma de Yucatán

### Facultad de Matemáticas

---

## Objetivo: Generar un compilador del lenguaje de programación "Tan"

Basándose en el lenguaje minilang descrito en clase

---

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

2. Para compilar tu propio código Tan desde Python:

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

---

## Descripción de tokens

### Palabras reservadas

- `xiib` (let)
- `tsiibil` (print)
- `keet` (=)

### Token de números

- `.` es 1
- `|` es 5
- `0` es 0
- Para los separadores de bloques se usa `,` (múltiplos de 20)
- Siempre primero los puntos, luego las barras

#### Ejemplos

- `..||` es el 12
- `0 , .` es el 20
- `..|, ..` es el 47
- `0 , 0 , 0 , 0 , .` es el 160,000

---

## Gramática del lenguaje de programación

```bnf
<program>    ::= <statement> { <statement> }
<statement>  ::= "xiib" <identifier> "keet" <expression>
              |   "tsiibil" "[" <expression> "]"
<expression> ::= <term> { ("+" | "-") <term> }
<term>       ::= <factor> { ("*" | "/") <factor> }
<factor>     ::= NUMBER | IDENT | "[" <expression> "]"
```

#### Ejemplo

```tan
xiib x keet |
xiib y keet . , .|
tsiibil [x + y * ..]
```

---

## Entregables

Entregar código con:

- Análisis léxico
- Análisis sintáctico
- Generador de código
- Casos de ejemplo positivos y negativos
