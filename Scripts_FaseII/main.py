from controllers import CustomerRentalController

def main():
    # Inicializa el director de orquesta de la arquitectura MVC
    app = CustomerRentalController()
    # Arranca el bucle principal del ERP
    app.run()

if __name__ == "__main__":
    main()