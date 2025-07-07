import inlcude.copiler as copiler
# Caso 1: Ejemplo básico del PDF
print("Caso 1: Ejemplo basico del PDF")
ejemplo1 = """
    xiib x keet |
    xiib y keet . , .|
    tsiibil [x + y * ..]
    """
compiled = copiler.compile_tan(ejemplo1)
if compiled:
    print("\n--- Ejecutando codigo compilado ---")
    exec(compiled)
