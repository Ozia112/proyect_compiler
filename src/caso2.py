import inlcude.copiler as copiler
# Caso 2: Operaciones mas complejas
print("\n\nCaso 2: Operaciones mas complejas")
ejemplo2 = """
    xiib a keet ..||
    xiib b keet . , 0
    xiib c keet a + b
    tsiibil [c]
    tsiibil [a * .. - b / |]
    """
compiled = copiler.compile_tan(ejemplo2)
if compiled:
    print("\n--- Ejecutando codigo compilado ---")
    exec(compiled)
 