import inlcude.copiler as copiler
# Caso 4: Error sintactico - falta keet
print("Caso 4: Error sintactico - falta 'keet'")
ejemplo_error1 = """
    xiib x |
    """
copiler.compile_tan(ejemplo_error1)