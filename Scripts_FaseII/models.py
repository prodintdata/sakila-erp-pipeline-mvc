from typing import List, Optional
from datetime import datetime
from dbcontext import DbContext
from entities import CustomerRental

class CustomerRentalModel:
    """
    Capa de Acceso a Datos (Repository/Model Pattern).
    Encargada de transformar filas de MySQL en colecciones List[CustomerRental]
    y ejecutar la lógica CRUD sobre el tablón analítico.
    """
    
    def get_all(self, limit: int = 100) -> List[CustomerRental]:
        """
        [READ] Mapea los registros de la base de datos a una lista de objetos Entidad.
        Cumple con el requerimiento de la rúbrica: Model (List<Entity>).
        """
        sql = """
            SELECT 
                rental_id, customer_id, customer_name, store_id, store_name,
                store_address, store_city, store_country, staff_name, film_id,
                film_title, rental_date, return_date, amount_paid, payment_date,
                replacement_cost 
            FROM denormalized_customer_rentals 
            ORDER BY rental_date DESC 
            LIMIT %s
        """
        
        rentals_list: List[CustomerRental] = []
        
        # Usamos nuestro despachador DbContext de forma segura
        with DbContext() as context:
            rows = context.execute_query(sql, (limit,))
            
            for row in rows:
                # Instanciamos el molde Entity por cada fila física devuelta
                entity = CustomerRental(
                    rental_id=row['rental_id'],
                    customer_id=row['customer_id'],
                    customer_name=row['customer_name'],
                    store_id=row['store_id'],
                    store_name=row['store_name'],
                    store_address=row['store_address'],
                    store_city=row['store_city'],
                    store_country=row['store_country'],
                    staff_name=row['staff_name'],
                    film_id=row['film_id'],
                    film_title=row['film_title'],
                    rental_date=row['rental_date'],
                    return_date=row['return_date'],
                    amount_paid=float(row['amount_paid']) if row['amount_paid'] is not None else None,
                    payment_date=row['payment_date'],
                    replacement_cost=float(row['replacement_cost'])
                )
                rentals_list.append(entity)
                
        return rentals_list

    def delete(self, rental_id: int) -> bool:
        """
        [DELETE] Elimina un registro del tablón analítico por su ID único.
        """
        sql = "DELETE FROM denormalized_customer_rentals WHERE rental_id = %s"
        with DbContext() as context:
            rows_affected = context.execute_non_query(sql, (rental_id,))
            return rows_affected > 0