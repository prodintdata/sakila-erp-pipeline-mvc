from dbcontext import DbContext

try:
    with DbContext() as context:
        print("¡Prueba exitosa! DbContext se conectó correctamente a MySQL.")
except Exception as e:
    print(f"Fallo en la prueba de infraestructura: {e}")