from General import Craft
from Pressures import Pressure
from Plating import Plating
from Stiffeners import Stiffener

def main():
    print("\nCalculadora de Escantillones - 'Scantlings Calculator'\n")
    # Crear una instancia de la clase Craft
    craft = Craft()
    # Crear una instancia de la clase Pressure, pasando el objeto craft
    pressure = Pressure(craft)
    # Crear una instancia de la clase Plating, pasando los objetos craft y pressure
    plating = Plating(craft, pressure)
    # Crear una instancia de la clase Stiffeners, pasando los objetos craft y pressure
    stiffener = Stiffener(craft, pressure)
    if craft.context == 'Plating':
        # Diccionario de métodos para las zonas de plating
        zone_plating_methods = {
            'Fondo': plating.bottom_plating,
            'Costados y Espejo': plating.side_transom_plating,
            'Cubierta': plating.deck_plating,
            'Superestructura': plating.superstructures_deckhouses_plating,
            'Mamparos estancos': plating.watertight_bulkheads_plating,
            'Mamparos de tanques integrales': plating.integral_tank_bulkheads_plating,
            'Placas anti oleaje': plating.wash_plates_plating,
            'Mamparos de colisión': plating.collision_bulkheads_plating
        }
        # Obtener y llamar al método adecuado según la zona seleccionada para plating
        selected_plating_method = zone_plating_methods.get(craft.zone)
        if selected_plating_method:
            print(f"Espesor para {craft.zone} (Plating): {selected_plating_method()}")
            
    # Obtener y llamar al método adecuado según la zona seleccionada para stiffeners
    elif craft.context == 'Stiffeners':
        print(f"Parámetros para los refuerzos de {craft.zone}: {stiffener.stiffeners()}, para: {craft.material}")
        
    else:
        print(f"Zona '{craft.zone}' no reconocida o no implementada.")
if __name__ == "__main__":
    main()