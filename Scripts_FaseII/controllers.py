import os
from datetime import datetime
from models import CustomerRentalModel
from entities import CustomerRental
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
        """Arranca el bucle principal de la aplicación (Menú Ejecutivo CRUD)."""
        while True:
            self.clear_screen()
            print("========================================================")
            print("         PRODINTDATA - SISTEMA ERP SAKILA V2.5          ")
            print("               ARQUITECTURA NATIVA MVC/ORM              ")
            print("========================================================")
            print(" [1] Visualizar Historial de Rentas (Read)")
            print(" [2] Insertar Nueva Transacción de Renta (Create)")
            print(" [3] Actualizar Renta Existente (Update)")
            print(" [4] Eliminar Registro de Renta (Delete)")
            print(" [5] Ejecutar Auditoría y Analítica Avanzada (Inferencia)")
            print(" [6] Salir del Sistema")
            print("========================================================")
            
            opcion = input("Seleccione una opción operativa (1-6): ").strip()
            
            if opcion == "1":
                self.handle_read()
            elif opcion == "2":
                self.handle_create()
            elif opcion == "3":
                self.handle_update()
            elif opcion == "4":
                self.handle_delete()
            elif opcion == "5":
                self.handle_analytics()
            elif opcion == "6":
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

    def handle_create(self) -> None:
        """Manejador del flujo de creación e inserción masiva a través del ORM."""
        self.clear_screen()
        print("========================================================")
        print("          REGISTRO DE NUEVA TRANSACCIÓN (CREATE)        ")
        print("========================================================")
        
        try:
            # Captura de datos obligatorios e identidad
            rental_id = int(input("Ingrese ID único de Renta (rental_id): ").strip())
            customer_id = int(input("Ingrese ID de Cliente (customer_id): ").strip())
            customer_name = input("Nombre Completo del Cliente: ").strip()
            
            # Datos de la Sucursal
            store_id = int(input("ID de Tienda (1 o 2): ").strip())
            store_country = input("País de la Tienda (Canada / Australia): ").strip()
            store_city = input("Ciudad de la Tienda: ").strip()
            store_name = f"Tienda {store_id} - {store_city}"
            store_address = input("Dirección Física de la Tienda: ").strip()
            
            # Datos Logísticos del Producto
            staff_name = input("Nombre del Empleado que Atendió: ").strip()
            film_id = int(input("ID de la Película (film_id): ").strip())
            film_title = input("Título de la Película: ").strip()
            
            # Variables Financieras y Temporales
            amount_paid = float(input("Monto Cobrado (USD): ").strip())
            replacement_cost = float(input("Costo de Reemplazo del Inventario (USD): ").strip())
            
            # Construcción de la Entidad con fechas automáticas del sistema
            nueva_renta = CustomerRental(
                rental_id=rental_id, customer_id=customer_id, customer_name=customer_name,
                store_id=store_id, store_name=store_name, store_address=store_address,
                store_city=store_city, store_country=store_country, staff_name=staff_name,
                film_id=film_id, film_title=film_title, rental_date=datetime.now(),
                return_date=None, amount_paid=amount_paid, payment_date=datetime.now(),
                replacement_cost=replacement_cost
            )
            
            print("\nSTATUS: Enviando objeto Entidad estructurado al Modelo...")
            if self.model.create(nueva_renta):
                print(f"SUCCESS: Transacción de renta {rental_id} guardada con éxito en la base de datos.")
            else:
                print("CONTROL: La base de datos rechazó la inserción del objeto.")
                
        except ValueError:
            print("\nERROR: Entrada de datos no válida. Verifique que los IDs y montos sean numéricos.")
        except Exception as e:
            print(f"ERROR: Ocurrió un fallo en el proceso de creación: {e}")
            
        input("\nPresione Enter para regresar al menú principal...")

    def handle_update(self) -> None:
        """Manejador del flujo de actualización de registros existentes."""
        self.clear_screen()
        print("========================================================")
        print("         MODIFICACIÓN DE CAMPOS FINANCIEROS (UPDATE)    ")
        print("========================================================")
        
        try:
            rental_id = int(input("Ingrese el ID de la renta que desea actualizar: ").strip())
            
            print("\nSTATUS: Recolectando los nuevos parámetros operativos...")
            staff_name = input("Nuevo Nombre del Empleado encargado: ").strip()
            amount_paid = float(input("Monto Final Corregido (USD): ").strip())
            replacement_cost = float(input("Nuevo Costo de Reemplazo (USD): ").strip())
            
            # Instanciamos una entidad temporal de actualización empaquetando los cambios
            entidad_update = CustomerRental(
                rental_id=rental_id, customer_id=0, customer_name="", store_id=0,
                store_name="", store_address="", store_city="", store_country="",
                staff_name=staff_name, film_id=0, film_title="", rental_date=datetime.now(),
                return_date=datetime.now(), amount_paid=amount_paid, payment_date=datetime.now(),
                replacement_cost=replacement_cost
            )
            
            print("\nSTATUS: Solicitando actualización de campos al Modelo...")
            if self.model.update(entidad_update):
                print(f"SUCCESS: Los campos financieros de la renta {rental_id} han sido consolidados.")
            else:
                print(f"CONTROL: No se encontró ningún registro bajo el ID {rental_id} para actualizar.")
                
        except ValueError:
            print("\nERROR: Los montos o identificadores deben poseer un formato numérico válido.")
        except Exception as e:
            print(f"ERROR: Fallo en la capa de control al actualizar: {e}")
            
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
            ejecutar_analisis_avanzado_sakila()
        except Exception as e:
            print(f"ERROR: Fallo al inicializar el componente analítico: {e}")
        
        input("\nAnálisis finalizado. Presione Enter para regresar al menú principal...")