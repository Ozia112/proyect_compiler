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

### Ejemplos de números

- `..||` = 12 (2 puntos + 2 barras = 2 + 10)
- `0 , .` = 20 (0×20¹ + 1×20⁰)
- `..|, ..` = 47 (7×20⁰ + 2×20¹)
- `0 , 0 , 0 , 0 , .` = 160,000



### Tabla de contenidos

- [Documentación:](/doc/)
  - [Documentación](/doc/doc.md)
  - [Compilador de ejemplo](/doc/ejemplocopiler.py)
  - [Instrucciones de uso](/doc/instrucciones.md)
- [Source:](/src/)
  - [Include/](/src/inlcude/)
    - [Biblioteca copiler.py](/src/inlcude/copiler.py)
  - Casos:
    - [Caso 1](/src/caso1.py)
    - [Caso 2](/src/caso2.py)
    - [Caso 3](/src/caso3.py)
  - Casos de error  
    - [Error caso 1](/src/caso_error1.py)
    - [Error caso 2](/src/caso_error2.py)
    - [Error caso 3](/src/caso_error3.py)
- [Assets:](/assets/) (No usados)
  - [Fuente con numeros mayas .ttf](/assets/NotoSansMayanNumerals-Regular.ttf)
  - [Excel convertidor dec to vig](/assets/Libro1.xlsx)

## 👥 Autores

- **Edrei Enrique Lizama Solis**
- **Isaac Alejandro Ortiz Zaldivar**
- **Ricardo Esteban Maas Tuyub**

<p align="center">
  Hecho con ❤️ en Mérida, Yucatán 🇲🇽
</p>
