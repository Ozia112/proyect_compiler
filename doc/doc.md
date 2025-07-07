# Documentación Técnica del Compilador del Lenguaje Tan

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Compilador](#arquitectura-del-compilador)
3. [Análisis Léxico](#análisis-léxico)
4. [Análisis Sintáctico](#análisis-sintáctico)
5. [Generación de Código](#generación-de-código)
6. [Función Principal](#función-principal)
7. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Introducción

El **Lenguaje Tan** es un lenguaje de programación experimental diseñado específicamente para incorporar elementos de la cultura maya yucateca. Este compilador implementa un sistema de numeración maya (base 20) y utiliza palabras en lengua maya para las operaciones basicas de programación.

### Características Principales

- **Sistema numérico maya**: Utiliza sistema vigesimal símbolos tradicionales
- **Sintaxis maya**: Palabras reservadas en lengua maya yucateca
- **Compilación a Python**: Genera código Python ejecutable
- **Arquitectura modular**: Separación clara entre análisis léxico, sintáctico y generación de código

---

## Arquitectura del Compilador

El compilador sigue el flujo de tres fases:

``` mermaid
graph LR
    A("Código Fuente (Tan)") --> B["Análisis Léxico"]
    B --> C["Análisis Sintáctico"]
    C --> D["Generación de Código"]
    D --> E["Python"]
```

### Flujo de Procesamiento

1. **Entrada**: Código fuente en Lenguaje Tan
2. **Tokenización**: Conversión a tokens usando expresiones regulares
3. **Parsing**: Construcción del Árbol Sintáctico Abstracto (AST)
4. **Generación**: Traducción del AST a código Python
5. **Salida**: Código Python ejecutable

---

## Análisis Léxico

### 1. Función `maya_to_decimal(maya_num)`

#### Propósito `maya_to_decimal(maya_num)`

Convierte una cadena sacada de la tokenizacion que representa un número maya en su valor decimal, respetando la notación posicional vigesimal.

#### Sistema de Numeración Maya

| Símbolo | Valor |
|---------|-------|
| `.`     | 1     |
| `\|`     | 5     |
| `0`     | 0     |
| `,`     | Separador de bloques (potencias de 20) |

#### Proceso de conversion

- Función:

  ```py
  def maya_to_decimal(maya_num):
  ```

- Secuencia de la funcion

  - Primero se eliminan los espacios que pudieran encontrarse en la expresion númerica:  
  
    ```py
      maya_num = maya_num.strip()  
    ```

  - Si el numero es 0, retorna 0:  

    ```py
      if maya_num == '0':
          return 0  
    ```

  - Dividir por comas para obtener bloques y almacenarlo en `blocks`:

    ```py
      blocks = maya_num.split(',')
    ```
  
  - Se buscan una lista de bloques donde cada bloque es una cadena que representa un numero usando los valores preestablecidos para 1, 5 y 0.
  - Para cada bloque el codigo elimina primero los espacios:

    ```py
      for block in blocks:
          block = block.strip()
    ```
  
  - Despues buscando la cantidad de puntos barras y cero los va sumando en variables que funcionan a modo de contadores:

    ```py
      for block in blocks:
          # codigo inicial...    
          dots = block.count('.')
          bars = block.count('|')
          zeros = block.count('0')
    ```

  - Si en el bloque hay un 0, no puede haber otro valor por lo tanto se establece `block_value` en 0, de lo contrario se suman la cantidad de puntos y la cantidad de barras multiplicadas por 5 asi nos da el valor del bloque:

    ```py
    # despues de contar la cantidad de puntos, barras y ceros:
      if zeros > 0:
          block_value = 0
      else:    
          block_value = dots + (bars * 5)
    ```

  - Despues calculamos el total de todos los bloques sumandolos y multiplicandolos con su respectiva potencia(base 20):

    ```py
      total += block_value * (20 ** power)
    ```

  - La potencia maxima es decir la que va a potenciar el bloque de mas a la izquierda, fue calculada previamente simplemente calculando la longitud de la cadena -1, mas adelante despues de cada iteracion se ajustaba restandole 1 al valor actual en el ciclo:

    ```py
      power = len(blocks) - 1
      # La potencia luego es ajustada con:
      power -= 1
    ```

  - Por último la función retorna `total`:

    ```py
      return total
    ```

- Ejemplos de conversion:
  - `.|` = 1 + 5 = **6**
  - `||` = 5 + 5 = **10**
  - `|` , `.` = (5 × 20¹) + (1 × 20⁰) = 100 + 1 = **101**
  - `.` , `||` , `...` = (1 × 20²) + (10 × 20¹) + (3 × 20⁰) = 400 + 200 + 3 = **603**

### 2. Especificación de Tokens

- **Definición de Tokens**  
Utilizando el modulo `re`(regex) de python, creamos un array que define una lista de tuplas, donde cada tupla tiene el nombre del token y una expresion regular que lo decribe:

  ```py
    token_specification = [
        ('MAYA_NUM', r'(?:[.|]+\s*|0)(?:\s*,\s*(?:[.|]+\s*|0))*'),
        ('XIIB',     r'xiib'),
        ('TSIIBIL',  r'tsiibil'),
        ('KEET',     r'keet'),
        ('IDENT',    r'[a-zA-Z_]\w*'),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('TIMES',    r'\*'),
        ('DIVIDE',   r'/'),
        ('LPAREN',   r'\['),
        ('RPAREN',   r'\]'),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
  ```

Tabla de tokens:

| Nombre | Descripción |
|---------|-------|
| `MAYA_NUM` | Reconoce números en notaicon maya (puntos, barras, ceros y comas) |
| `XIIX` `TSIIBIL` `KEET` | Palabras reservadas del lenguaje |
| `IDENT` | Identificadores(nomrbes de variables) |
| `PLUS` `MINUS` `TIMES` `DIVIDE` | Operadores matemáticos |
| `LPAREN` `RPAREN` | Corchetes usados como paréntesis |
| `NEWLINE` | Saltos de linea |
| `SKIP` | Espacios y tabulaciones (se ignoran) |
| `MISMATCH` | Cualquier otro carácter (deteccion de errores) |

- **Contruccion de expresion regular general:**  
Con las definiciones realizadas en `token_specification` se realiza la union general de todas las re con `.join` almacenandolos en tok_regex.

### 3. Función `tokenize(code)`

#### Propósito de `tokenize(code)`

Realiza el análisis léxico del código fuente, convirtiendo la secuencia de caracteres en una lista estructurada de tokens.

#### Proceso de Tokenización

- Primero, se inicializa el array vacío `tokens`, donde se almacenarán los tokens generados.
- El ciclo `for mo in re.finditer(tok_regex, code):` itera sobre todas las coincidencias de la expresión regular en el código fuente (`code`).
  - `mo` es un objeto de coincidencia (match object) del módulo `re`.
- La variable `kind` almacena el tipo de token que coincidió, según los especificados previamente.
- La variable `value` almcena el texto exacto del código fuente (`code`) que coincidió con el token.
- En el caso de que kind == `MAYA_NUM`:
  - Se convierte el valor maya a decimal usando la funcion `maya_to_decimal(value)`.
  - Se agrega a la lista de tokens una tupla con el tipo `NUMBER` y el valor decimal.

    ```py
      if kind == 'MAYA_NUM':
          decimal_value = maya_to_decimal(value)
          tokens.append(('NUMBER', decimal_value))
    ```

- Para las palabras resevadas `xiib`, `tsiibil`, `keet` y los operadores, estos son almacenados con su tipo y valor.
- Para los tokens de tipo `IDENT` (nombres de variables), estos pueden ser cualquier combinación alfanumérica, exceptuando las palabras reservadas. Se almacenan como `IDENT` junto con su valor.

  ```py
      elif kind == 'IDENT':
          if value not in ['xiib', 'tsiibil', 'keet']:
              tokens.append(('IDENT', value))
  ```

- Los tokens de tipo `NEWLINE` y `SKIP` (espacios y tabulaciones) se ignoran.

  ```py
      elif kind in ('NEWLINE', 'SKIP'):
          continue
  ```

- Al final del ciclo, si se encuentra un token de tipo `MISMATCH`, imprime un mensaje de error con el texto "Caracter inesperado (caracter)".

  ```py
      elif kind == 'MISMATCH':
          raise RuntimeError(f'Caracter inesperado {value!r}')
  ```

- Por último reotrna el arreglo `tokens`.

#### Salida de tokens generados

- El resultado se imprime en la consla con la siguiente estructura:

  ```console
  Ejemplo con "xiib x keet ."
    Tokens generados:
      ('XIIB', 'xiib')
      ('IDENT', 'x')
      ('KEET', 'keet')
      ('NUMBER', 1)
  ```

---

## Análisis Sintáctico

### Gramática Formal del Lenguaje Tan

La **gramática formal** define las reglas que indican cómo deben organizarse los elementos del Lenguaje Tan para formar programas válidos. Especifica cómo se combinan los tokens para crear sentencias y expresiones correctas.

La BNF permite definir de manera precisa las posibles construcciones del lenguaje mediante reglas de producción recursivas.

A continuación se presenta la gramática BNF del Lenguaje Tan, que cubre declaraciones, expresiones aritméticas y la precedencia de operadores. Esta gramática es la base para el análisis sintáctico y la construcción del Árbol Sintáctico Abstracto (AST) durante la compilación.

```bnf
<program>    ::= <statement> { <statement> }
<statement>  ::= "xiib" <identifier> "keet" <expression> |  "tsiibil" "[" <expression> "]"
<expression> ::= <term> { ("+" | "-") <term> }
<term>       ::= <factor> { ("*" | "/") <factor> }
<factor>     ::= NUMBER | IDENT | "[" <expression> "]"
```

- Jerarquia de operadores

1. **Paréntesis**: `[ ]` (máxima jerarquía)
2. **Multiplicación/División**: `*`, `/`
3. **Suma/Resta**: `+`, `-` (mínima jerarquía)

### Clase `Parser`

#### Arquitectura

Implementa un **analizador sintáctico descendente recursivo** que construirá el Árbol Sintáctico Abstracto (AST) mediante el método de descenso recursivo.

#### Métodos Principales

##### `__init__(self, tokens)`

- **Función**: Inicializa el parser con la lista de tokens
- **Estado**: Mantiene posición actual en la secuencia de tokens

##### `consume(self, expected_type=None)`

```python
def consume(self, expected_type=None):
    """
    Consume el token actual y avanza la posición.
    Valida que el token sea del tipo esperado.
    """
```

- **Validación**: Verifica concordancia de tipos
- **Manejo de errores**: Genera `SyntaxError` descriptivos
- **Retorno**: Token consumido

##### `peek(self)`

```python
def peek(self):
    """
    Examina el token actual sin consumirlo.
    Utilizado para decisiones de parsing.
    """
```

##### `parse(self)`

- **Función**: Punto de entrada principal del análisis sintáctico
- **Proceso**: Parsea secuencia completa de statements
- **Retorno**: Lista de nodos AST

##### `statement(self)`

Parsea declaraciones completas del lenguaje:

- **Tipo 1: Asignación**

```py
xiib <identificador> keet <expresión>
```

Genera: `('assign', nombre_variable, expresión_ast)`

- **Tipo 2: Impresión**

```py
tsiibil [<expresión>]
```

Genera: `('print', expresión_ast)`

##### `expression(self)`, `term(self)`, `factor(self)`

Implementan la jerarquía de precedencia de operadores mediante recursión mutua:

- **`expression`**: Maneja `+` y `-` (asociatividad izquierda)
- **`term`**: Maneja `*` y `/` (mayor precedencia)
- **`factor`**: Elementos atómicos (números, variables, expresiones parentizadas)

#### Ejemplo de Construcción de AST

```py
Entrada: xiib suma keet . + |
         ↓
Tokens:  [('XIIB', 'xiib'), ('IDENT', 'suma'), ('KEET', 'keet'), 
          ('NUMBER', 1), ('PLUS', '+'), ('NUMBER', 5)]
         ↓
AST:     ('assign', 'suma', ('plus', ('number', 1), ('number', 5)))
```

---

## Generación de Código

### Arquitectura del Generador

El módulo de generación de código traduce el AST a código Python ejecutable mediante un recorrido del árbol sintáctico.

### Funciones del Generador

#### `generate_python(ast)`

```python
def generate_python(ast):
    """
    Genera código Python completo a partir del AST.
    Procesa lista de statements y los concatena.
    """
```

- **Entrada**: Lista de nodos AST
- **Proceso**: Mapeo secuencial de cada statement
- **Salida**: Código Python como string

#### `gen_stmt(node)`

```python
def gen_stmt(node):
    """
    Genera código Python para declaraciones individuales.
    """
```

**Mapeo de Declaraciones:**

- `('assign', variable, expresión)` → `"variable = expresión"`
- `('print', expresión)` → `"print(expresión)"`

#### `gen_expr(expr)`

```python
def gen_expr(expr):
    """
    Genera código Python para expresiones.
    Maneja recursivamente expresiones anidadas.
    """
```

**Mapeo de Expresiones:**

- `('number', valor)` → `"valor"`
- `('var', nombre)` → `"nombre"`
- `('plus', izq, der)` → `"(izq + der)"`
- `('minus', izq, der)` → `"(izq - der)"`
- `('times', izq, der)` → `"(izq * der)"`
- `('divide', izq, der)` → `"(izq / der)"`

### Ejemplo Completo de Generación

#### Código Fuente Tan

```py
xiib resultado keet || + .
tsiibil [resultado]
```

#### AST Intermedio

```python
[
    ('assign', 'resultado', ('plus', ('number', 10), ('number', 1))),
    ('print', ('var', 'resultado'))
]
```

#### Código Python Generado

```python
resultado = (10 + 1)
print(resultado)
```

---

## Función Principal

### `compile_tan(code)`

#### Propósito de

Orquesta el proceso completo de compilación, integrando todas las fases del compilador y proporcionando información detallada de depuración.

#### Flujo de Ejecución

```python
def compile_tan(code):
    """
    Pipeline completo de compilación:
    1. Análisis léxico (tokenización)
    2. Análisis sintáctico (construcción AST)
    3. Generación de código Python
    4. Información de depuración
    """
```

#### Fases del Proceso

1. **Inicialización**
   - Imprime encabezado del compilador
   - Muestra código fuente original

2. **Análisis Léxico**

   ```python
   tokens = tokenize(code)
   print("Tokens generados:")
   for token in tokens:
       print(f"  {token}")
   ```

3. **Análisis Sintáctico**

   ```python
   parser = Parser(tokens)
   ast = parser.parse()
   print("Árbol Sintáctico Abstracto (AST):")
   for node in ast:
       print(f"  {node}")
   ```

4. **Generación de Código**

   ```python
   py_code = generate_python(ast)
   print("Código Python generado:")
   print(py_code)
   ```

5. **Manejo de Errores**
   - Captura excepciones en cualquier fase
   - Proporciona mensajes de error descriptivos
   - Retorna `None` en caso de fallo

#### Información de Depuración

La función proporciona visibilidad completa del proceso de compilación:

- **Código fuente original**
- **Lista detallada de tokens**
- **Estructura del AST**
- **Código Python resultante**
- **Mensajes de error específicos**

---

## Ejemplos de Uso

### Ejemplo 1: Declaración y Asignación Simple

#### Código Tan

``` py
xiib numero keet ||.
```

#### Proceso de Compilación

**Tokens:**

```py
[('XIIB', 'xiib'), ('IDENT', 'numero'), ('KEET', 'keet'), ('NUMBER', 11)]
```

**AST:**

```py
[('assign', 'numero', ('number', 11))]
```

**Python Generado:**

```python
numero = 11
```

### Ejemplo 2: Operaciones Aritméticas

#### Código Tan

```py
xiib calculo keet ||| + ..
tsiibil [calculo]
```

#### Proceso de Compilación

**Tokens:**

```py
[('XIIB', 'xiib'), ('IDENT', 'calculo'), ('KEET', 'keet'), 
 ('NUMBER', 15), ('PLUS', '+'), ('NUMBER', 2),
 ('TSIIBIL', 'tsiibil'), ('LPAREN', '['), ('IDENT', 'calculo'), ('RPAREN', ']')]
```

**AST:**

```py
[('assign', 'calculo', ('plus', ('number', 15), ('number', 2))),
 ('print', ('var', 'calculo'))]
```

**Python Generado:**

```python
calculo = (15 + 2)
print(calculo)
```

### Ejemplo 3: Expresiones Complejas con Precedencia

#### Código Tan

```py
xiib resultado keet . + | * ..
```

#### Análisis de Precedencia

- La multiplicación `|` *`..` se evalúa primero (5* 2 = 10)
- Luego la suma `. +` (1 + 10 = 11)

**Python Generado:**

```python
resultado = (1 + (5 * 2))
```

### Ejemplo 4: Números Mayas Complejos

#### Código Tan

```py
xiib maya_grande keet |, |||
```

#### Conversión Maya

- `|` = 5 (primer bloque, posición 20¹)
- `|||` = 15 (segundo bloque, posición 20⁰)
- Resultado: (5 × 20) + 15 = 115

**Python Generado:**

```python
maya_grande = 115
```
