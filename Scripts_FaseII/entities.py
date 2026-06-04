from datetime import datetime
from typing import Optional

class CustomerRental:
    """
    Representa un objeto Entidad (espejo físico) de una fila 
    en la tabla analítica 'denormalized_customer_rentals'.
    """
    def __init__(
        self,
        rental_id: int,
        customer_id: int,
        customer_name: str,
        store_id: int,
        store_name: str,
        store_address: str,
        store_city: str,
        store_country: str,
        staff_name: str,
        film_id: int,
        film_title: str,
        rental_date: datetime,
        return_date: Optional[datetime],
        amount_paid: Optional[float],
        payment_date: Optional[datetime],
        replacement_cost: float
    ) -> None:
        # Atributos de Identidad de la Renta y Cliente
        self.rental_id: int = rental_id
        self.customer_id: int = customer_id
        self.customer_name: str = customer_name
        
        # Atributos Geográficos e Identidad de la Tienda
        self.store_id: int = store_id
        self.store_name: str = store_name
        self.store_address: str = store_address
        self.store_city: str = store_city
        self.store_country: str = store_country
        
        # Atributos Logísticos y del Producto
        self.staff_name: str = staff_name
        self.film_id: int = film_id
        self.film_title: str = film_title
        self.rental_date: datetime = rental_date
        self.return_date: Optional[datetime] = return_date
        
        # Atributos Financieros Reales Auditanles
        self.amount_paid: Optional[float] = amount_paid
        self.payment_date: Optional[datetime] = payment_date
        self.replacement_cost: float = replacement_cost

    def __repr__(self) -> str:
        """Permite imprimir el objeto en consola."""
        fecha_pago = self.payment_date.strftime('%Y-%m-%d') if self.payment_date else "Sin Pago"
        return (f"<CustomerRental ID: {self.rental_id} | "
                f"Cliente: {self.customer_name} | "
                f"Tienda: {self.store_city} | "
                f"Monto: USD {self.amount_paid} | "
                f"Fecha Pago: {fecha_pago}>")