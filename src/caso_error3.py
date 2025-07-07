import inlcude.copiler as copiler
# Caso 6: Error lexico - caracter invalido
print("\n\nCaso 6: Error lexico - caracter invalido")
ejemplo_error3 = """
    xiib x keet @
    """
copiler.compile_tan(ejemplo_error3)