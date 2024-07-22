"""
    Main de la calculadora de ISO 12215-5
"""

from validations import val_data

class Craft:
    def __init__(self, material):
        self.diseñador = input("Diseñador: ")
        self.boat = input("Embarcación: ")
        self.empresa = input("Empresa: ")
        self.gerencia = input("Gerencia: ")
        self.division = input("División: ")
        self.values = {}
        self.material = self.get_material()
        self.zonas = self.get_zonas(material)
        

    def get_value(self, key, prompt, *args) -> float:
        if key not in self.values:
            self.values[key] = val_data(prompt, *args)
        return self.values[key]

    def display_menu(self, items) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def get_material(self) -> int:
        if 'material' not in self.values:
            print("\nLista de materiales disponibles")
            materiales = ('Acero', 'Aluminio', 'Aluminio extruido', 'Aluminio en Sandwich', 'Aluminio Corrugado', 'Fibra laminada', 'Fibra en sandwich')
            self.display_menu(materiales)
            choice = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(materiales))
            self.values['material'] = choice
        return self.values['material']

    def get_zonas(self, material) -> list:
        if 'zonas' not in self.values:
            zonas = {
                1: 'Vagra Maestra',
                2: 'Casco de Fondo',
                3: 'Casco de Costado',
                4: 'Espejo de Popa',
                5: 'Cubierta de Principal',
                6: 'Cubiertas Inferiores/Otras Cubiertas',
                7: 'Cubiertas Humedas',
                8: 'Cubiertas de Superestructura y Casetas de Cubierta',
                9: 'Mamparos Estancos',
                10: 'Mamparos de Tanques Profundos',
                11: 'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos',
                12: 'Túneles de Waterjets',
                13: 'Túneles de Bow Thrusters',
                14: 'Cubiertas de Operación o Almacenamiento de Vehículos'
            }
            if material == 1:
                zonas = zonas
            else:
                zonas = zonas
            self.display_menu(zonas)
            choice = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(zonas))
            self.values['zonas'] = choice
        return self.values['zonas']
    
    
        
        