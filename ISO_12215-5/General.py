"""
    Main de la calculadora de ISO 12215-5
    
    Intentar hacer una sola funcion que calcule el pressure y luego el thickeness de una para cada zona,
    es decir, funcion por zona en donde se calcule la presion y luego el espesor tomando como parametro el material y la zona
    
class Scantlings:

    def init(self, craft):
        self.craft = craft

    def calculate_scantling (material, zone):
        if zone == bottom:
            thickness = def bottom_Scantling (material):
            return thickness
            
    def bottom_scantling (material): $VOY POR ESTA$
        pressure = def calculate_pressure (material, zone):
        
        if material == acero_aluminio:
            thickness = def acero_aluminio_plating (pressure, zone):
            return thickness
    
def bottom_scantling (material):
    planning =24 * mLDC + 4
    slamming = 12 * mLDC + 4
    pressure = max(planning, slamming)
    
    if material == acero_aluminio:
        thickness = def acero_aluminio_plating (pressure, zone):
        return thickness
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
            materiales = ('Acero', 'Aluminio', 'Fibra laminada', 'Fibra con nucleo (Sandwich)')
            self.display_menu(materiales)
            choice = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(materiales))
            self.values['material'] = choice
        return self.values['material']
    
    def get_zones(self) -> list:
        if 'selected_zones' not in self.values:
            zonas = {
                1: 'Casco de Fondo',
                2: 'Casco de Costado',
                3: 'Espejo de Popa',
                4: 'Cubierta de Principal',
                5: 'Cubiertas Inferiores/Otras Cubiertas',
                6: 'Cubiertas Humedas',
                7: 'Cubiertas de Superestructura y Casetas de Cubierta',
                8: 'Mamparos Estancos',
                9: 'Mamparos de Tanques Profundos',
                10: 'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos',
                11: 'Túneles de Waterjets',
                12: 'Túneles de Bow Thrusters',
                13: 'Cubiertas de Operación o Almacenamiento de Vehículos'
            }

            available_zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] if self.material not in [1, 2] else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
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
    
    def get_Z(self) -> float:
        return self.get_value('Z', "Altura de francobordo (metros): ")
    
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
    
    def get_hB(self) -> float:
        return val_data("Altura de la columna de agua (metros): ")
    
    
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
    
    def get_b(self, zone) -> float:
        return val_data(f"Longitud mas corta de los paneles de la zona {zone} (mm): ")
    
    def get_l(self, zone) -> float:
        #b = self.get_b(zone) #Revisar esto porque si no se guarda en diccionario se volveria a pedir b innecesariamente
        return val_data(f"Longitud mas larga de los paneles de la zona {zone} (mm): ", True, True, 0)
    
    def get_s(self, zone ) -> float:
        return val_data(f"Separación del alma o viga longitudinal, rigidizador, transversal, etc. de la zona: {zone} (metros): ")
    
    def get_lu(self, zone) -> float:
        #s = self.get_s(zone)
        return val_data(f"Luz o espacio entre refuerzos de la zona {zone} (mm): ", True, True, 0) #Longitud del alma longitudinal, rigidizador, transversal o viga
    
    def get_c(self, zone) -> float:
        return val_data(f"Corona o curvatura del panel/refuerzo de la zona {zone} (mm): ")
    
    def get_x(self) -> float:
        LH = self.get_LH()
        return val_data("Distancia longitudinal desde popa hasta el punto de analisis (metros): ", True, True, LH, 0)
    

class Scantlings:
    
    def __init__(self, craft, pressures, plating):
        #Composisción de la clase Craft
        self.craft = craft
        self.pressure = pressures
        self.plating = plating
        
        
    def calculate_scantling(self, material, zone):
        if zone == 1:
            thickness = self.bottom_scantling(material, zone)
            return thickness
        elif zone == 2:
            thickness = self.side_scantling(material, zone)
            return thickness
        elif zone == 3:
            thickness = self.deck_scantling(material, zone)
            return thickness
    
    def bottom_scantling(self, material, zone):
        #craft_type = self.craft.get_craft_type()
        
        LWL = self.craft.get_LWL()
        BC = self.craft.get_BC()
        mLDC = self.craft.get_mLDC()
        V = self.craft.get_V()
        B04 = self.craft.get_B04()
        
        b = self.craft.get_b(zone)
        l = self.craft.get_l(zone)
        s = self.craft.get_s(zone)
        lu = self.craft.get_lu(zone)
        c = self.craft.get_c(zone)
        x = self.craft.get_x()
        
        bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.pressure.calculate_pressure(material, zone, LWL, BC, mLDC, V, B04, b, l, s, lu, x)
        thickness = self.plating.calculate_plating(material, zone, bottom_pressure_plating, b, l, c) #calcular el thickeness de esta manera con una funcion general o tener una funcion especifica para cada material como pressures
        #stiffeners = self.stiffeners.calculate_stiffeners(zone)
        return thickness

    def side_scantling(self, material, zone):
        LWL = self.craft.get_LWL()
        BC = self.craft.get_BC()
        mLDC = self.craft.get_mLDC()
        
        b = self.craft.get_b(zone)
        l = self.craft.get_l(zone)
        s = self.craft.get_s(zone)
        lu = self.craft.get_lu(zone)
        x = self.craft.get_x()
        
        side_pressure_plating, side_pressure_stiffeners = self.pressure.calculate_side_pressure(LWL, BC, mLDC, b, l, s, lu, x)
        thickness = self.plating.calculate_thickness(material, zone, side_pressure_plating)
        #stiffeners = self.stiffeners.calculate_stiffeners(zone)
        return thickness
    
class Pressures:
    
    def __init__(self, craft):
        self.craft = craft
        
        
    def calculate_pressure(self, material, zone, LWL, BC, mLDC, V, B04, b, l, s, lu, x):
        if zone == 1:
            bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.bottom_pressure(material, zone, LWL, BC, mLDC, V, B04, b, l, s, lu, x)
            return bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners
        elif zone == 2:
            pressure, index = self.side_pressure()
            return pressure, index
        elif zone == 3:
            pressure, index = self.deck_pressure()
            return pressure, index
        elif zone == 4:
            pressure = self.superstructures_deckhouses_pressure()
            return pressure, 0
        elif zone == 5:
            pressure = self.watertight_bulkheads_pressure()
            return pressure, 0
        elif zone == 6:
            pressure = self.integral_tank_bulkheads_pressure()
            return pressure, 0
        elif zone == 7:
            pressure = self.wash_plates_pressure()
            return pressure, 0
        elif zone == 8:
            pressure = self.collision_bulkheads_pressure()
            return pressure, 0
        elif zone == 9:
            pressure = self.nonwatertight_partial_bulkheads_pressure()
            return pressure, 0
        elif zone == 10:
            pressure = self.transmission_pillar_loads_pressure()
            return pressure, 0
        else:
            return "Zona no está en la base de datos"

    def design_category_factor_kDC(self) -> float:
        # Asegurarse de que la categoría de diseño ya está definida a través de la instancia de 'craft'
        design_category = self.craft.get_design_category()
        
        # Mapeo de categoría de diseño a valores de kDC
        kDC_values = {'A': 1.0, 'B': 0.8, 'C': 0.6, 'D': 0.4}
        
        # Retornar el valor correspondiente de kDC
        return kDC_values[design_category]
    
    def dynamic_load_factor_nCG(self, LWL, BC, mLDC, V, B04) -> float:
        """
        Calcula el factor de carga dinámica nCG para embarcaciones de motor en modo de planeo.
        Retorna:
        float: El valor de nCG, limitado a un máximo de 7.
        """

        # Calcular nCG usando la ecuación (1)
        nCG_1 = 0.32 * ((LWL / (10 * BC)) + 0.084) * (50 - B04) * ((V**2 * BC**2) / mLDC)
        
        # Calcular nCG usando la ecuación (2)
        nCG_2 = (0.5 * V) / (mLDC**0.17)
        
        # Determinar el valor de nCG
        if nCG_1 > 3:
            nCG = min(nCG_1, nCG_2)
        else:
            nCG = nCG_1  # Si nCG_1 es menor o igual a 3, lo usamos directamente
        
        # Limitar nCG a un máximo de 7
        nCG = min(nCG, 7)
        
        # Imprimir una advertencia si nCG es mayor que 7 (aunque este caso no debería ocurrir dado el min anterior)
        if nCG > 7:
            print(f"\nCUIDADO: El valor de carga dinámica (nCG)= {nCG} no debe ser mayor a 7, revise sus parámetros iniciales")
        
        return nCG

    def longitudinal_pressure_factor_kL(self, LWL, BC, mLDC, V, B04, x) -> float:
        """
        Parámetros:
            x (float): Posición longitudinal a lo largo de la longitud de la línea de flotación (LWL),
            medida desde el extremo de popa.
        """
        xLWL = x / LWL  # Calcula la relación x/LWL
        
        if xLWL > 0.6:
            kL = 1.0  # Si x/LWL es mayor que 0.6, kL es 1.0
        else:
            nCG = self.dynamic_load_factor_nCG(LWL, BC, mLDC, V, B04)  # Calcular nCG
            nCG_clamped = min(max(nCG, 3.0), 6.0)  # Limitar nCG entre 3 y 6
            
            # Aplica la ecuación para valores de x/LWL <= 0.6
            kL = ((1 - 0.167 * nCG_clamped) * (xLWL / 0.6)) + (0.167 * nCG_clamped)
            kL = min(kL, 1.0)  # Asegurarse de que kL no sea mayor que 1.0
        
        return kL

    def area_pressure_factor_kAR(self, material, mLDC, b, l, s, lu) -> tuple:
        """
        Calcula el valor de kAR ajustado al material y limitado a un máximo de 1 para Plating y Stiffeners.
        """
        craft_type = self.craft.get_craft_type()  # Tipo de embarcación
        
        # Cálculo de AD para Plating y Stiffeners
        AD_plating = min((l * b) * 1e-6, 2.5 * (b**2) * 1e-6)
        AD_stiffeners = max((lu * s) * 1e-6, 0.33 * (lu**2) * 1e-6)
        
        # Determinación de kR según el tipo de embarcación
        if craft_type == 'planning_craft':
            kR_plating = 1
            kR_stiffeners = 1
        else:
            kR_plating = 1.5 - 3e-4 * b
            kR_stiffeners = 1 - 2e-4 * lu
        
        # Cálculo de kAR para Plating
        kAR_plating = (kR_plating * 0.1 * (mLDC**0.15)) / (AD_plating**0.3)
        kAR_plating = min(kAR_plating, 1)  # kAR no debe ser mayor que 1
        
        # Cálculo de kAR para Stiffeners
        kAR_stiffeners = (kR_stiffeners * 0.1 * (mLDC**0.15)) / (AD_stiffeners**0.3)
        kAR_stiffeners = min(kAR_stiffeners, 1)  # kAR no debe ser mayor que 1
        
        # Ajustes basados en el material
        if material == 'Fibra con nucleo (Sandwich)':
            min_kAR = 0.4
        elif material == 'Fibra laminada':
            min_kAR = 0.25
        else:
            min_kAR = 0
        
        # Aplicación de los mínimos ajustados según el material
        kAR_plating = max(min_kAR, kAR_plating)
        kAR_stiffeners = max(min_kAR, kAR_stiffeners)
        
        # Retornar ambos valores
        return kAR_plating, kAR_stiffeners
  
    def hull_side_pressure_factor_kZ(self) -> tuple:
        Z = self.craft.get_Z()
        h_plating = val_data("Ingrese la altura del centro del panel por encima de la linea de flotación (metros): ", True, True, 0, 0, Z)
        h_stiffeners = val_data("Ingrese la altura del centro del refuerzo por encima de la linea de flotación (metros): ", True, True, 0, 0, Z)
        
        kZ_platting = (Z-h_plating)/Z
        kZ_stiffeners = (Z-h_stiffeners)/Z
        
        return kZ_platting, kZ_stiffeners
    
    def superstructure_deckhouse_pressure_factor_kSUP(self) -> float:
        # Devuelve un diccionario con todos los valores de kSUP
        kSUP_values = {
            'Frente': 1,
            "Lateral (Área de Paso)": 0.67,
            "Lateral (Área de No Paso)": 0.5,
            'A Popa': 0.5,
            "Superior <= 800 mm sobre cubierta": 0.5, # Área caminada
            "Superior > 800 mm sobre cubierta": 0.35, # Área caminada
            #"Niveles Superiores": 0 (REVISAR)                  # Elementos no expuestos al clima ###REVISAR
        }
        return kSUP_values
    
    #Pressure Zones
    def bottom_pressure(self, material, zone, LWL, BC, mLDC, V, B04, b, l, s, lu, x) -> tuple:
        """
        Calcula la presión de fondo para Plating y Stiffeners, e indica si fue tomada en modo de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de fondo para Plating, Presión de fondo para Stiffeners, Estado de Plating (Desplazamiento/Planeo), Estado de Stiffeners (Desplazamiento/Planeo)
        """
        # Declaramos los factores necesarios para la presión de fondo
        nCG = self.dynamic_load_factor_nCG(LWL, BC, mLDC, V, B04)
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(material, mLDC, b, l, s, lu)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL(LWL, BC, mLDC, V, B04, x)
        
        # Se calculan valores base y minimos de la presión de fondo en modo de desplazamiento y planeo
        PBMD_BASE = 2.4 * (mLDC**0.33) + 20
        PBMP_BASE = ((0.1 * mLDC)/(LWL * BC))*((1 + kDC**0.5) * nCG)
        PBM_MIN = 0.45 * (mLDC ** 0.33) + (0.9 * LWL * kDC)
        
        # Calcula la presión de fondo en modo de desplazamiento
        PBMD_plating = PBMD_BASE * kAR_plating * kDC * kL
        PBMD_stiffeners = PBMD_BASE * kAR_stiffeners * kDC * kL
        
        # Asegúrate de que la presión no sea inferior al mínimo
        PBMD_plating = max(PBM_MIN, PBMD_plating)
        PBMD_stiffeners = max(PBM_MIN, PBMD_stiffeners)

        # Calcula la presión de fondo en modo de planeo
        PBMP_plating = PBMP_BASE * kAR_plating * kDC * kL
        PBMP_stiffeners = PBMP_BASE * kAR_stiffeners * kDC * kL
        
        # Asegúrate de que la presión no sea inferior al mínimo
        PBMP_plating = max(PBM_MIN, PBMP_plating)
        PBMP_stiffeners = max(PBM_MIN, PBMP_stiffeners)

        # Siempre usa la mayor presión de fondo entre desplazamiento y planeo
        bottom_pressure_plating = max(PBMD_plating, PBMP_plating)
        bottom_pressure_stiffeners = max(PBMD_stiffeners, PBMP_stiffeners)

        # Índice para indicar si se utilizó la presión en modo de planeo o desplazamiento
        index_plating = "planning" if bottom_pressure_plating == PBMP_plating else "displacement"
        index_stiffeners = "planning" if bottom_pressure_stiffeners == PBMP_stiffeners else "displacement"
        
        return bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners

    def side_pressure(self, LWL, BC, mLDC, b, l, s, lu, x) -> tuple:
        """
        Calcula la presión de costado para Plating y Stiffeners según las categorías de diseño y modos de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de costado para Plating, Presión de costado para Stiffeners.
        """
        design_category = self.craft.get_design_category()
        
        # Declaramos los factores necesarios para la presión de costado
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(b, l, s, lu)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL(x)
        kZ_plating, kZ_stiffeners = self.hull_side_pressure_factor_kZ()
        
        # Se calculan valores base y minimos de la presión de costado en modo de desplazamiento y planeo
        PDM_BASE = 0.35 * LWL + 14.6
        PBMD_BASE = 2.4 * (mLDC**0.33) + 20
        PBMP_BASE = ((0.1 * mLDC) / (LWL * BC)) * ((1 + kDC**0.5) * nCG)
        PSM_MIN = 0.9 * LWL * kDC
        
        # Categorías A y B: Comparamos PSMD y PSMP y tomamos el mayor
        if design_category in ['A', 'B']:
            # Calcula la presión de costado en modo de desplazamiento
            PSMD_plating = (PDM_BASE + kZ_plating * (PBMD_BASE - PDM_BASE)) * kAR_plating * kDC * kL
            PSMD_stiffeners = (PDM_BASE + kZ_stiffeners * (PBMD_BASE - PDM_BASE)) * kAR_stiffeners * kDC * kL
            
            # Asegúrate de que la presión no sea inferior al mínimo
            PSMD_plating = max(PSM_MIN, PSMD_plating)
            PSMD_stiffeners = max(PSM_MIN, PSMD_stiffeners)
            
            # Calcula la presión de costado en modo de planeo
            PSMP_plating = (PDM_BASE + kZ_plating * (0.25 * PBMP_BASE - PDM_BASE)) * kAR_plating * kDC * kL
            PSMP_stiffeners = (PDM_BASE + kZ_stiffeners * (0.25 * PBMP_BASE - PDM_BASE)) * kAR_stiffeners * kDC * kL
            
            # Asegúrate de que la presión no sea inferior al mínimo
            PSMP_plating = max(PSM_MIN, PSMP_plating)
            PSMP_stiffeners = max(PSM_MIN, PSMP_stiffeners)
            
            # Siempre usa la mayor presión de costado entre desplazamiento y planeo
            side_pressure_plating = max(PSMD_plating, PSMP_plating)
            side_pressure_stiffeners = max(PSMD_stiffeners, PSMP_stiffeners)

        # Categorías C y D: La presión del costado depende del modo donde la presión del fondo es mayor
        else:
            print("\nCategoría C y D: La presión del costado depende del modo donde la presión del fondo es mayor")
            bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.bottom_pressure(LWL, BC, mLDC, b, l, s, lu, x)
            
            if index_plating == "planeo":
                # Si la presión de fondo mayor es la de planeo, usamos PSMP para Plating
                PSMP_plating = (PDM_BASE + kZ_plating * (0.25 * PBMP_BASE - PDM_BASE)) * kAR_plating * kDC * kL
                side_pressure_plating = max(PSM_MIN, PSMP_plating)
            else:
                # Si la presión de fondo mayor es la de desplazamiento, usamos PSMD para Plating
                PSMD_plating = (PDM_BASE + kZ_plating * (PBMD_BASE - PDM_BASE)) * kAR_plating * kDC * kL
                side_pressure_plating = max(PSM_MIN, PSMD_plating)

            if index_stiffeners == "planeo":
                # Si la presión de fondo mayor es la de planeo, usamos PSMP para Stiffeners
                PSMP_stiffeners = (PDM_BASE + kZ_stiffeners * (0.25 * PBMP_BASE - PDM_BASE)) * kAR_stiffeners * kDC * kL
                side_pressure_stiffeners = max(PSM_MIN, PSMP_stiffeners)
            else:
                # Si la presión de fondo mayor es la de desplazamiento, usamos PSMD para Stiffeners
                PSMD_stiffeners = (PDM_BASE + kZ_stiffeners * (PBMD_BASE - PDM_BASE)) * kAR_stiffeners * kDC * kL
                side_pressure_stiffeners = max(PSM_MIN, PSMD_stiffeners)
        
        return side_pressure_plating, side_pressure_stiffeners
    
    def deck_pressure(self, LWL, b, l, s, lu, x):
        """
        Calcula la presión sobre la cubierta para Plating y Stiffeners.
        Retorna:
            tuple: Presión sobre la cubierta para Plating y Stiffeners, asegurando que no sea inferior a un valor mínimo.
        """
        # Obtener los factores de ajuste de la presión
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(b, l, s, lu)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_distribution_kL(x)
        
        # Valores base para la presión en la cubierta
        PDM_BASE = 0.35 * LWL + 14.6
        PDM_MIN = 5  # Presión mínima permitida
        
        # Cálculo de la presión de la cubierta para Plating y Stiffeners
        PDM_plating = PDM_BASE * kAR_plating * kDC * kL
        PDM_stiffeners = PDM_BASE * kAR_stiffeners * kDC * kL
        
        # La presión de cubierta no debe ser inferior al valor mínimo
        deck_pressure_plating = max(PDM_MIN, PDM_plating)
        deck_pressure_stiffeners = max(PDM_MIN, PDM_stiffeners)
        
        return deck_pressure_plating, deck_pressure_stiffeners

    def superstructure_deckhouses_pressure(self, LWL, b, l, s, lu):
        """
        Calcula la presión sobre las superestructuras y casetas de cubierta para Plating y Stiffeners.
        Retorna:
            tuple: Presión sobre las superestructuras y casetas de cubierta para Plating y Stiffeners.
        """
        # Factores de ajuste de la presión
        kDC = self.design_category_factor_kDC()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(b, l, s, lu)
        kSUP = self.superstructure_kSUP()  # Factor para superestructuras y casetas
        
        # Valor base de presión para superestructuras y casetas
        PDM_BASE = 0.35 * LWL + 14.6
        PDM_MIN = 5  # Presión mínima permitida
        
        # Cálculo de presión para Plating y Stiffeners
        PSUP_plating = PDM_BASE * kDC * kAR_plating * kSUP
        PSUP_stiffeners = PDM_BASE * kDC * kAR_stiffeners * kSUP
        
        # Asegurar que la presión no sea menor al valor mínimo permitido
        superdeck_pressure_plating = max(PDM_MIN, PSUP_plating)
        superdeck_pressure_stiffeners = max(PDM_MIN, PSUP_stiffeners)
        
        return superdeck_pressure_plating, superdeck_pressure_stiffeners
    
    def watertight_bulkheads_pressure(self, hB):
        """ Presión para mamparos estancos. """
        PWB = 7 * hB
        return PWB
    
    def integral_tank_bulkheads_pressure(self, hB):
        """ Presión para mamparos de tanques integrales. """
        PTB = 10 * hB
        return PTB

class Plating:
    def __init__(self, craft):
        self.craft = craft
        self.k1 = 0.017        

    def calculate_plating(self, material, zone, pressure, b, l, c):
        if material == 1:
            return self.steel_thickness(zone, pressure, b, l, c)
        elif material == 2:
            return self.aluminum_thickness(zone, pressure, b, l, c)
        elif material == 3:
            thickness = self.single_skin_plating(zone, pressure, b, l, c)
            return thickness
        elif material == 4:
            return self.fiber_core_plating(zone, pressure)
        
    def curvature_correction_kC(self, b, c):
        cb = c / b
        if cb <= 0.03:
            kC = 1.0
        elif cb <= 0.18 and cb > 0.03: #Ajustado
            kC = 1.1 - (3.33 * c) / b
        else:  # cb > 0.18
            kC = 0.5
        # Aplica las restricciones de que kC no debe ser menor a 0.5 ni mayor a 1.0
        kC = max(min(kC, 1.0), 0.5)
        return kC
    
    def steel_thickness(self, zone, pressure, b, l, c):
        kC = self.curvature_correction_kC(b, c)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        sigma_u = self.craft.get_sigma_u()
        sigma_y = self.craft.get_sigma_y() #Voy po raqui definir sigma
        sigma_d = 0.5 * self.craft.get_sigma_uf()
        thickness = b * kC * np.srt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def aluminum_thickness(self, zone, pressure, b, l, c):
        pass
    
    def single_skin_plating(self, zone, pressure, b, l, c):
        kC = self.curvature_correction_kC(b, c)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        sigma_d = 0.5 * self.craft.get_sigma_uf()
        thickness = b * kC * np.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def fiber_core_plating(self,zone, pressure):
        pass
    
    def wash_plates_plating(self):
        return self.craft.superstructure_deckhouses_pressure()[1]
    
    def watertight_bulkheads_plating(self):
        return self.craft.watertight_bulkheads_pressure()


def main():
    print("ESCANTILLONADO ISO 12215-5 - ISO 12215-5 SCANTLINGS\n")
    craft = Craft()
    pressures = Pressures(craft)
    plating = Plating(craft)
    scantling = Scantlings(craft, pressures, plating)
    values = {}

    # Calcular el espesor para cada zona
    for zone in craft.selected_zones:
        thickness = scantling.calculate_scantling(craft.material, zone)
        
        # Almacenar el espesor calculado para cada zona en el diccionario
        if thickness is not None:
            values[zone] = thickness
        else:
            print(f"Error: No se pudo calcular el espesor para la zona {zone}")

    # Imprimir los espesores de todas las zonas calculadas
    for zone, thickness in values.items():
        print(f"El espesor requerido en la zona {zone} es de: {thickness:.3f} mm")

if __name__ == "__main__":
    main()
