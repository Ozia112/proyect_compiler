# Proyecto Integrador - Teoría de la Computación

## Universidad Autónoma de Yucatán
### Facultad de Matemáticas

---

## Objetivo: Generar un compilador del lenguaje de programación "tan"

Basándose en el lenguaje minilang descrito en clase

### a. Descripción de tokens

#### Palabras reservadas
- `xiib` (let)
- `tsiibil` (print)
- `keet` (=)

#### Token de números
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

### b. Gramática del lenguaje de programación

```
<program>    ::= <statement> { <statement> }

<statement>  ::= "xiib" <identifier> "ASSIGN" <expression>
             |   "tsiibil" "LPAREN" <expression> "RPAREN"

<expression> ::= <term> { ["PLUS" | "MINUS"] <term> }

<term>       ::= <factor> { ["TIMES" | "DIVIDE"] <factor> }

<factor>     ::= "NUMBER"
             |   "IDENT"
             |   "LPAREN" <expression> "RPAREN"
```

#### Ejemplo

```
xiib x keet |
xiib y keet . , .|
tsiibil [x + y * ..]
```

### Entregables

Entregar código con:
- Análisis léxico
- Análisis sintáctico
- Generador de código
- Casos de ejemplo positivos y negativos