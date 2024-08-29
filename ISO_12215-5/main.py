"""
    Main de la calculadora de ISO 12215-5
"""

import numpy as np
from validations import val_data

class Craft:
    
    
    def __init__(self):
        self.designer_name = input("Diseñador: ")
        self.boat_name = input("Embarcación: ")
        self.company_name = input("Empresa: ")
        self.management_name = input("Gerencia: ")
        self.division_name = input("División: ")
        self.values = {}
        self.design_category = self.get_design_category()
        self.material = self.get_material()
        self.selected_zones = self.get_zones()
        

    #Metodo para pedir datos y validar si ya existe
    def get_value(self, key, prompt, *args) -> float:
        if key not in self.values:
            self.values[key] = val_data(prompt, *args)
        return self.values[key]

    #Metodo para mostrar info solo para consola
    def display_menu(self, items) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def get_design_category(self) -> str:
        if 'categoria_diseño' not in self.values:
            print("\nSeleccione la categoría de diseño de la embarcación")
            categoria_diseño = ('Oceano', 'Offshore', 'Costera', 'Aguas calmadas')
            self.display_menu(categoria_diseño)
            choice = val_data("Ingrese el número correspondiente: ", False, True, -1, 1, len(categoria_diseño))
            
            # Mapeo de la selección a la categoría de diseño
            categorias = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
            self.values['categoria_diseño'] = categorias[choice]
            
        return self.values['categoria_diseño']
    
    def get_material(self) -> int:
        if 'material' not in self.values:
            print("\nLista de materiales disponibles")
            materiales = ('Acero', 'Aluminio', 'Fibra laminada', 'Fibra en sandwich')
            self.display_menu(materiales)
            choice = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(materiales))
            self.values['material'] = choice
        return self.values['material']
    
    def get_zones(self) -> list:
        if 'selected_zones' not in self.values:
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

            available_zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] if self.material not in [1, 2] else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            print("\nSeleccione las zonas que desea escantillonar\n")
        
            # Mostrar las zonas disponibles desde una lista
            for number in available_zones:
                print(f"{number}. {zonas[number]}")
            selected_zones = []
            while True:
                try:
                    choice = int(input("\nIngrese el número correspondiente y presione Enter\n(ingrese '0' para finalizar)\n-> "))
                    if choice == 0:
                        if not selected_zones:
                            raise ValueError("Debe seleccionar al menos una zona antes de finalizar.")
                        break
                    elif choice in available_zones:
                        if choice in selected_zones:
                            raise ValueError("Zona ya seleccionada, elija otra.")
                        selected_zones.append(choice)
                        print(f"Añadida: {zonas[choice]}")
                    else:
                        print("Selección no válida, intente de nuevo.")
                except ValueError as e:
                    print(e)
            self.values['selected_zones'] = selected_zones
        return self.values['selected_zones']
    
    
    """PRINCIPAL CRAFT DATA"""
    def get_BC(self) -> float:
        LWL = self.get_LWL()
        return self.get_value('BC', f"Manga entre pantoques ó 'Chine beam' a {0.4 * LWL} metros de la popa (metros): ")
    
    def get_BH(self) -> float:
        return self.get_value('BH', "Manga del casco (metros): ")
    
    def get_BWL(self) -> float:
        return self.get_value('BWL', "Manga de flotación (metros): ")
     
    def get_Db(self) -> float:
        return self.get_value('Db', "Profundidad del mamparo (metros): ")
    
    def get_LH(self) -> float:
        return self.get_value('LH', "Eslora del casco (metros): ", True, True, -1, 2.5, 24)

    def get_LWL(self) -> float:
        LH = self.get_LH()
        return self.get_value('LWL', "Eslora de flotación (metros): ", True, True, -1, 0, LH)

    def get_V(self) -> float:
        LWL = self.get_LWL()
        min_speed = 2.26 * np.sqrt(LWL)
        return self.get_value('V', f"Velocidad máxima (nudos, debe ser >= {min_speed:.2f}): ", True, True, -1, min_speed)

    def get_mLDC(self) -> float:
        return self.get_value('mLDC', "Desplazamiento de la embarcación (kg): ")

    def get_B04(self) -> float:
        LWL = self.get_LWL()
        B04 = self.get_value('B04', f"Ángulo de astilla muerta fondo a {0.4 * LWL:.2f} metros de la popa (°grados): ")
        
        if B04 < 10 or B04 > 30:
            print(f"Advertencia: El ángulo de astilla muerta {B04}° está fuera del rango sugerido (10° a 30°).")
        return B04
    
    def get_craft_type(self) -> str:
        # Obtener la velocidad y eslora de flotación
        V = self.get_V()
        LWL = self.get_LWL()

        # Determinar el tipo de embarcación basado en la relación V/LWL
        if V / np.sqrt(LWL) >= 5:
            craft_type = "planning_craft"
        else: # V / LWL < 5
            craft_type = "displacement_craft"

        # Si no está almacenado, lo añadimos a values
        if 'craft_type' not in self.values:
            self.values['craft_type'] = craft_type

        # Devolvemos el tipo de embarcación
        return self.values['craft_type']
    
    # def get_D(self) -> float:
    #     return self.get_value('D', "Puntal (metros): ")

    # def get_d(self) -> float:
    #     L = self.get_L()
    #     D = self.get_D()
    #     return self.get_value('d', "Calado (metros): ", True, True, 0, 0.04 * L, D)
    
    
    
    """PANEL/STIFFENER DIMENSIONS"""
    
    """CALCULATION DATA: FACTOR, PRESSURES, PARAMETERS, STRESSES"""
    # def get_tau(self) -> float:
    #     return self.get_value('tau', "Ángulo de trimado a velocidad máxima (grados): ", True, True, -1, 3)
    
    def get_h13(self) -> float:
        L = self.get_L()
        tipo_embarcacion = self.get_tipo_embarcacion()
        h13_values = {1: 4, 2: 2.5, 3: 0.5, 4: 4}
        h13 = max(h13_values.get(tipo_embarcacion), (L / 12))
        return h13
    
    def get_sigma_y(self) -> float:
        return self.get_value('sigma_y', "Limite elastico por tracción del material (MPa): ")
    
    def get_sigma_u(self) -> float:
        return self.get_value('sigma_u', "Esfuerzo ultimo a la tracción del material (MPa): ")
    
    def get_sigma_uf(self) -> float:
        return self.get_value('sigma_uf', "Resistencia mínima a la flexión (MPa): ")
    
    def get_sigma_uo(self) -> float:
        return self.get_value('sigma_uo', "Resistencia a la tracción de la fibra externa (MPa): ")
    
    def get_sigma_ui(self) -> float:
        return self.get_value('sigma_ui', "Resistencia a la tracción de la fibra interna (MPa): ")
    
    def get_sigma_ub(self) -> float:
        return self.get_value('sigma_ub', "Menor de las resistencias a la tracción o a la compresión (MPa): ")
    
    def get_s(self, zone, context) -> float:
        if context == 'Plating':
            return val_data(f"Longitud mas corta de los paneles de la zona {zone} (mm): ")
        else:
            return val_data(f"Separación del alma o viga longitudinal, rigidizadora, transversal, etc. de la zona {zone} (metros): ")
    
    def get_l(self, zone, context, s) -> float:
        if context == 'Plating':
            return val_data(f"Longitud mas larga de los paneles de la zona {zone} (mm): ", True, True, 0, s)
        else:
            return val_data(f"Longitud del alma longitudinal, rigidizadora, transversal o viga de la zona {zone} (mm): ", True, True, 0, s)
     
     
class Pressures:
    
    def __init__(self, craft) -> None:
        self.craft = craft
        self.kDC = self.calculate_kDC()

    def calculate_kDC(self) -> float:
        # Asegurarse de que la categoría de diseño ya está definida a través de la instancia de 'craft'
        design_category = self.craft.get_design_category()
        
        # Mapeo de categoría de diseño a valores de kDC
        kDC_values = {'A': 1.0, 'B': 0.8, 'C': 0.6, 'D': 0.4}
        
        # Retornar el valor correspondiente de kDC
        return kDC_values[design_category]

