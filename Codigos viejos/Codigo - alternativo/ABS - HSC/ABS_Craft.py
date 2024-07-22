from validations import val_data
from typing import List

class Craft:

    MATERIALS: List[str] = ['Acero', 'Aluminio', 'FRP - single skin', 'FRP - sandwich']
    ZONES: List[str] = ['Cuaderna Maestra', 'Fondo', 'Costado', 'Cubiertas, Mamparos y Superestructura']

    def __init__(self):
        print("\nCalculadora de Escantillonado ABS --- 'ABS - Scantlings'\n")
        self.L = val_data("\nIngrese la eslora de escantillón (metros): ")
        self.LW = val_data("Ingrese la eslora de la línea de flotación (metros): ")
        self.B = val_data("\nIngrese la manga de su embarcación (metros): ")
        self.BW = val_data("Ingrese la manga de la línea de flotación (metros): ")
        self.D = val_data("\nIngrese el puntal de su embarcacion (metros): ")
        self.d = val_data("\nIngrese el calado de la embarcación (metros): ")
        self.V = val_data("\nIngrese la velocidad (Nudos): ")
        self.W = val_data("\nIngrese el desplazamiento de la embarcación (Toneladas): ") * 1000
        self.Bcg = val_data("\nIngrese la astilla muerta fondo en LCG (°grados): ")
        self.material = self.calculate_material()
        self.sigma_u = val_data("\nIngrese el esfuerzo ultimo a la tracción (MPa): ")
        self.sigma_y = val_data("Ingrese el limite elastico por tracción (MPa): ")
        self.resistencia = self.determine_resistencia()
        self.zone = self.select_zone()
        self.sigma_ap = self.dstress_plating(self.zone)
        self.sigma_ai = self.dstress_internals(self.zone)

    def display_menu(self, items: List[str]) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def calculate_material(self) -> str:
        """Calcula y devuelve el material seleccionado para la embarcación."""
        print("\nLista de materiales disponibles:")
        self.display_menu(self.MATERIALS)
        opcion = val_data("Seleccione un material (Ingrese el número correspondiente): ", False, True, 0, 1, len(self.MATERIALS))
        material = self.MATERIALS[opcion - 1]
        return material

    def determine_resistencia(self) -> str:
        """Determina la resistencia del material."""
        if self.material == 'Acero':
            if 200 < self.sigma_y < 300:
                return 'Ordinaria'
            elif 300 <= self.sigma_y:
                return 'Alta'
            else:
                return 'Baja'
        return 'Ordinaria'

    def select_zone(self) -> str:
        """Permite al usuario seleccionar una zona."""
        print("\nSeleccione la zona donde desea realizar los calculos")
        self.display_menu(self.ZONES)
        choice = val_data("Ingrese el número correspondiente: ", False, True, 0, 1, len(self.ZONES))
        return self.ZONES[choice - 1]

    def dstress_plating(self, zone) -> tuple:
        """Calcula el esfuerzo de diseño basado en la zona seleccionada."""
        zones = {
            'Fondo': {
                'Bottom Shell Slamming Pressure': 0.90 * self.sigma_y,
                'Bottom Shell Hydrostatic Pressure': 0.55 * self.sigma_y,
            },
            'Costado': {
                'Side Shell Slamming Pressure': 0.90 * self.sigma_y,
                'Side Shell Hydrostatic Pressure': 0.55 * self.sigma_y,
            },
            'Cubiertas, Mamparos y Superestructura': {
                'Deck Plating Strength Deck': 0.60 * self.sigma_y,
                'Deck Plating Lower Decks/Other Decks': 0.60 * self.sigma_y,
                'Deck Plating Wet Decks': 0.90 * self.sigma_y,
                'Bulkheads Deep Tank': 0.60 * self.sigma_y,
                'Bulkheads Watertight': 0.95 * self.sigma_y
            }
        }
        if zone == 'Cuaderna Maestra':
            zone = 'Fondo'
        selected_zone = zones[zone]
        stress_values = tuple(selected_zone.values())
        return stress_values

    def dstress_internals(self, zone) -> tuple:
        """Calcula el esfuerzo de diseño basado en la zona seleccionada."""
        zones = {
            'Fondo': {
                'Bottom Longitudinals Slamming Pressure': 0.65 * self.sigma_y,
                'Bottom Transverse and Girders Slamming pressure': 0.80 * self.sigma_y,
                'Bottom Longitudinals Sea Pressure': 0.50 * self.sigma_y,
                'Bottom Transverses and Girders Sea pressure': 0.60 * self.sigma_y
            },
            'Costado': {
                'Side Longitudinals Slamming Pressure': 0.60 * self.sigma_y,
                'Side Transverses and Girders Slamming Pressure': 0.80 * self.sigma_y,
                'Side Longitudinals Sea Pressure': 0.50 * self.sigma_y,
                'Side Transverses and Girders Sea Pressure': 0.60 * self.sigma_y,
            },
            'Cubiertas, Mamparos y Superestructura': {
                'Deck Longitudinals - Strength Decks': 0.33 * self.sigma_y,
                'Deck Longitudinals - Other Decks': 0.40 * self.sigma_y,
                'Deck Transverses and Girders Strength Decks': 0.75 * self.sigma_y,
                'Deck Transverses and Girders Other Decks': 0.75 * self.sigma_y, 
                'Wet Deck Longitudinals': 0.75 * self.sigma_y,
                'Wet Deck Transverses and Girders': 0.75 * self.sigma_y,
                'Watertight Bulkheads': 0.85 * self.sigma_y,
                'Tank Bulkheads': 0.60 * self.sigma_y,
                'Superstructure and Deckhouse': 0.70 * self.sigma_y
            },
        }
        if zone == 'Cuaderna Maestra':
            zone = 'Fondo'
        selected_zone = zones[zone]
        stress_values = tuple(selected_zone.values())
        return stress_values 
