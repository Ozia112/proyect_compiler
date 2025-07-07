import inlcude.copiler as copiler
# Caso 3: Numero grande
print("\n\nCaso 3: Numero grande")
ejemplo3 = """
    xiib grande keet . , 0 , 0 , 0 , 0
    tsiibil [grande]
    """
compiled = copiler.compile_tan(ejemplo3)
if compiled:
    print("\n--- Ejecutando codigo compilado ---")
    exec(compiled)
    