import inlcude.copiler as copiler
# Caso 5: Error sintactico - parentesis sin cerrar
print("\n\nCaso 5: Error sintactico - parentesis sin cerrar")
ejemplo_error2 = """
    xiib x keet |
    tsiibil [x + ..
    """
copiler.compile_tan(ejemplo_error2)