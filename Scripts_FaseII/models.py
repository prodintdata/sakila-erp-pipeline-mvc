from typing import List
from dbcontext import DbContext
from entities import CustomerRental

class CustomerRentalModel:
    """
    Capa de Acceso a Datos (Repository/Model Pattern).
    Encargada de transformar filas de MySQL en colecciones List[CustomerRental]
    y ejecutar la lógica CRUD completa sobre el tablón analítico.
    """
    
    def create(self, entity: CustomerRental) -> bool:
        """
        [CREATE] Inserta un nuevo registro en el tablón analítico a partir de un objeto Entidad.
        Recibe un CustomerRental completamente poblado y lo persiste en la BD.
        """
        sql = """
            INSERT INTO denormalized_customer_rentals (
                rental_id, customer_id, customer_name, store_id, store_name,
                store_address, store_city, store_country, staff_name, film_id,
                film_title, rental_date, return_date, amount_paid, payment_date,
                replacement_cost
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            entity.rental_id, entity.customer_id, entity.customer_name,
            entity.store_id, entity.store_name, entity.store_address,
            entity.store_city, entity.store_country, entity.staff_name,
            entity.film_id, entity.film_title, entity.rental_date,
            entity.return_date, entity.amount_paid, entity.payment_date,
            entity.replacement_cost
        )
        with DbContext() as context:
            rows_affected = context.execute_non_query(sql, params)
            return rows_affected > 0

    def get_all(self, limit: int = 100) -> List[CustomerRental]:
        """
        [READ] Mapea los registros de la base de datos a una lista de objetos Entidad.
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
        
        with DbContext() as context:
            rows = context.execute_query(sql, (limit,))
            for row in rows:
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

    def update(self, entity: CustomerRental) -> bool:
        """
        [UPDATE] Actualiza los campos financieros y logísticos de una renta existente.
        Usa rental_id como clave de búsqueda; solo modifica los campos que pueden cambiar.
        """
        sql = """
            UPDATE denormalized_customer_rentals
            SET
                return_date       = %s,
                amount_paid       = %s,
                payment_date      = %s,
                staff_name        = %s,
                replacement_cost  = %s
            WHERE rental_id = %s
        """
        params = (
            entity.return_date,
            entity.amount_paid,
            entity.payment_date,
            entity.staff_name,
            entity.replacement_cost,
            entity.rental_id
        )
        with DbContext() as context:
            rows_affected = context.execute_non_query(sql, params)
            return rows_affected > 0

    def delete(self, rental_id: int) -> bool:
        """
        [DELETE] Elimina un registro del tablón analítico por su ID único.
        """
        sql = "DELETE FROM denormalized_customer_rentals WHERE rental_id = %s"
        with DbContext() as context:
            rows_affected = context.execute_non_query(sql, (rental_id,))
            return rows_affected > 0