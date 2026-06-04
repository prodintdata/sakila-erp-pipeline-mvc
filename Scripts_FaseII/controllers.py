import os
from models import CustomerRentalModel
# Importamos el componente analítico avanzado de forma directa
from analytics_view import ejecutar_analisis_avanzado_sakila

class CustomerRentalController:
    """
    Componente Controlador (Patrón MVC).
    Dirige el flujo de la aplicación, interactúa con el Modelo
    y gestiona la experiencia del usuario en la interfaz.
    """
    def __init__(self) -> None:
        self.model = CustomerRentalModel()

    def clear_screen(self) -> None:
        """Limpia la consola según el sistema operativo para mantener el orden visual."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self) -> None:
        """Arranca el bucle principal de la aplicación (Menú Ejecutivo)."""
        while True:
            self.clear_screen()
            print("========================================================")
            print("         PRODINTDATA - SISTEMA ERP SAKILA V2.0          ")
            print("               ARQUITECTURA NATIVA MVC/ORM              ")
            print("========================================================")
            print(" [1] Visualizar Historial de Rentas (Mapeo ORM - Read)")
            print(" [2] Eliminar Registro de Renta (Control de Flujo - Delete)")
            print(" [3] Ejecutar Auditoría y Analítica Avanzada (Inferencia)")
            print(" [4] Salir del Sistema")
            print("========================================================")
            
            opcion = input("Seleccione una opción operativa (1-4): ").strip()
            
            if opcion == "1":
                self.handle_read()
            elif opcion == "2":
                self.handle_delete()
            elif opcion == "3":
                self.handle_analytics()
            elif opcion == "4":
                print("\nCerrando sesión de forma segura. Conexiones liberadas. Hasta pronto.")
                print("========================================================")
                break
            else:
                input("\nERROR: Opción no válida. Presione Enter para reintentar...")

    def handle_read(self) -> None:
        """Manejador del flujo de lectura de datos."""
        self.clear_screen()
        print("========================================================")
        print("          CONSULTA DE OPERACIONES LOGÍSTICAS            ")
        print("========================================================")
        
        try:
            limite_input = input("¿Cuántos registros desea extraer de la BD? (Por defecto 10): ").strip()
            limite = int(limite_input) if limite_input.isdigit() else 10
            
            print("\nSTATUS: Solicitando datos al Modelo...")
            rentas = self.model.get_all(limit=limite)
            
            print(f"\nSTATUS: Mapeo ORM Exitoso. Registros recuperados: {len(rentas)}")
            print("--------------------------------------------------------")
            
            for index, r in enumerate(rentas, 1):
                print(f"{index}. Cliente: {r.customer_name}")
                print(f"   Película: {r.film_title} | Alquilada en: {r.store_city} ({r.store_country})")
                print(f"   Monto: USD {r.amount_paid if r.amount_paid is not None else 0.00} | Rentado: {r.rental_date}")
                print("-" * 56)
                
        except Exception as e:
            print(f"ERROR: Fallo en la capa de control al leer datos: {e}")
            
        input("\nPresione Enter para regresar al menú principal...")

    def handle_delete(self) -> None:
        """Manejador del flujo de eliminación."""
        self.clear_screen()
        print("========================================================")
        print("         MODULO DE ELIMINACIÓN DE TRANSACCIONES         ")
        print("========================================================")
        
        rental_id_str = input("Ingrese el ID único de la renta (rental_id) a eliminar: ").strip()
        
        if not rental_id_str.isdigit():
            print("\nERROR: El ID debe ser un valor numérico entero.")
            input("Presione Enter para regresar...")
            return
            
        rental_id = int(rental_id_str)
        confirmacion = input(f"CONFIRMACION: ¿Está seguro que desea eliminar la renta ID {rental_id}? (S/N): ").strip().upper()
        
        if confirmacion == 'S':
            try:
                print("\nSTATUS: Comunicando orden de baja al Modelo...")
                exito = self.model.delete(rental_id)
                
                if exito:
                    print(f"SUCCESS: Registro {rental_id} eliminado físicamente de la base de datos.")
                else:
                    print(f"CONTROL: No se encontró ninguna renta activa con el ID {rental_id}.")
            except Exception as e:
                print(f"ERROR: Fallo operativo durante la eliminación: {e}")
        else:
            print("\nCANCELADO: Operación cancelada por el usuario. Base de datos intacta.")
            
        input("\nPresione Enter para regresar al menú principal...")

    def handle_analytics(self) -> None:
        """Manejador que dispara el motor de analítica e inferencia estadística."""
        self.clear_screen()
        try:
            # Llamamos directamente a la función del script analítico
            ejecutar_analisis_avanzado_sakila()
        except Exception as e:
            print(f"ERROR: Fallo al inicializar el componente analítico: {e}")
        
        input("\nAnálisis finalizado. Presione Enter para regresar al menú principal...")


