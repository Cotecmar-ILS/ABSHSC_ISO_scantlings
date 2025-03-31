"""Scantlings Design Calculator (SDC)"""
import math #Se puede quitar para optimizar y cuando se necesita calcular la raiz cuadrada, elevar a la 1/2. O exportar solo la raiz cuadrada
from validations import val_data

class Craft:
        
    # Mapeado de zonas y sus atributos
    ZONE_DIM = {
        'Casco de Fondo':      ['b', 'l', 's', 'lu', 'c', 'x'],                 #1
        'Casco de Costado':    ['b', 'l', 's', 'lu', 'c', 'x'],                 #2
        'Cubierta Superior':   ['b', 'l', 'c'],                                 #3
        'Superestructura y Casetas de Cubierta': ['b', 'l'],                    #4
        'Mamparos Estancos':   ['b', 'l', 's', 'lu', 'hB'],                     #5
        'Mamparos de Tanques / Colisiónes': ['b', 'l', 's', 'lu', 'hB']         #6
    }
    # 'Mamparos estructurales (No estancos)':['b', 'l', 's', 'lu', 'hB'],     #x
    
    def __init__(self, design_cat_index, material):
        # self.designer = designer
        # self.boat = boat
        # self.company = company
        # self.management = management
        # self.division = division
        self.design_cat_index = design_cat_index
        self.material = material
        # Principal Craft Data
        print("\nIngrese los atributos principales de la embarcación")
        self.LH = val_data("LH: Eslora del casco (metros): ", 2.5, 24)
        self.LWL = val_data("LWL:Eslora de flotación (metros): ", 1e-6, self.LH)
        self.BH = val_data("BH: Manga del casco (metros): ")
        self.BWL = val_data("BWL: Manga de flotación (metros): ", 1e-6, self.BH)
        self.BC = val_data(f"BC: Manga entre pantoques ('Chine beam') a {0.4 * self.LWL:.2f} metros de la popa (metros): ", 1e-6, self.BH)
        self.mLDC = val_data("mLDC: Desplazamiento de la embarcación en condición de plena carga (toneladas): ") * 1000
        self.V = self.get_V()
        self.B04 = self.get_B04()
        self.Z = val_data("Z: Altura del francobordo (metros): ")
        self.type = self.get_craft_type()
        
    def get_V(self) -> float:
        min_speed = 2.26 * math.sqrt(self.LWL)
        return val_data(f"V: Velocidad máxima en condición de plena carga (nudos, debe ser >= {min_speed:.2f}): ", min_speed)

    def get_B04(self) -> float:
        B04 = val_data(f"B0,4: Ángulo de astilla muerta de fondo a {0.4 * self.LWL:.2f} metros de la popa (°grados): ")
        if B04 < 10 or B04 > 30:
            print(f"Advertencia: El ángulo de astilla muerta {B04}° se tomó fuera del rango sugerido (10° a 30°).")
        return B04
        
    def get_craft_type(self) -> str:
        # Determinar el tipo de embarcación basado en la relación V/LWL
        if self.V / math.sqrt(self.LWL) >= 5:
            return "planning_craft"
        else: # V / LWL < 5
            return "displacement_craft"

class Zone:
    def __init__(self, craft, zone_name, zone_index):
        self.craft = craft
        self.zone_name = zone_name
        self.zone_index = zone_index
        # Llamamos inmediatamente a get_zone_dimensions para pedir los datos
        self.zone_attributes = self.get_zone_dimensions(zone_name)
        # Extraer de forma segura cada atributo del diccionario
        self.b = self.zone_attributes.get('b', None)
        self.l = self.zone_attributes.get('l', None)
        self.s = self.zone_attributes.get('s', None)
        self.lu =self.zone_attributes.get('lu', None)
        self.c = self.zone_attributes.get('c', None)
        self.x = self.zone_attributes.get('x', None)
        self.hB =self.zone_attributes.get('hB', None)
    
    """PANEL/STIFFENER DIMENSIONS"""
    # Definir las zonas y sus atributos dependientes
    def get_zone_dimensions(self, zone_name) -> dict:
        # Obtener la lista de atributos necesarios para la zona seleccionada
        required_attributes = self.craft.ZONE_DIM[zone_name]
        
        # Mapeado de funciones para solicitar cada atributo
        attribute_prompts = {
            'l': lambda: val_data(f"l: Longitud más larga de los paneles de la zona {zone_name} (mm): "),
            'b': lambda: val_data(f"b: Longitud más corta de los paneles de la zona {zone_name} (mm): ", 1e-6, min(zone_attributes.get('l', float('inf')), 330 * self.craft.LH)),
            'lu': lambda: val_data(f"lu: Luz o espacio entre refuerzos de la zona {zone_name} (mm): "),
            's': lambda: val_data(f"s: Separación del alma o viga longitudinal de la zona {zone_name} (mm): "),
            'c': lambda: val_data(f"c: Corona o curvatura del panel/refuerzo de la zona {zone_name} (mm): "),
            'x': lambda: val_data(f"x: Distancia longitudinal desde popa hasta el punto de análisis de la zona {zone_name} (metros): ", 0, self.craft.LH, self.craft.LH),
            'hB': lambda: val_data(f"hB: Altura de la columna de agua en la zona {zone_name} (mm): "),
        }
        
        # Solicitar los atributos de la zona
        print(f"\nIngrese los atributos correspondientes de la zona: {zone_name}")
        # Diccionario para almacenar los valores ingresados
        zone_attributes = {}
        # Recolectar los valores dinámicamente
        for attribute in required_attributes:
            zone_attributes[attribute] = attribute_prompts[attribute]()  # Llama a la función `lambda`

        return zone_attributes

class Pressures:
    
    def __init__(self, craft: object):
        self.craft = craft

    def calculate_pressure(self, zone):
        if zone.zone_index == 1:
            # Casco de fondo
            bottom_pressure_plating, bottom_pressure_stiffeners = self.bottom_pressure(zone)
            return bottom_pressure_plating, bottom_pressure_stiffeners
        elif zone.zone_index == 2:
            # Casco de costado
            side_pressure_plating, side_pressure_stiffeners = self.side_pressure(zone)
            return side_pressure_plating, side_pressure_stiffeners
        elif zone.zone_index == 3:
            # Cubierta superior
            deck_pressure_plating, deck_pressure_stiffeners = self.deck_pressure(zone)
            return deck_pressure_plating, deck_pressure_stiffeners
        elif zone.zone_index == 4:
            # Superestructura y casetas de cubierta
            superstructure_pressure_plating, superstructure_pressure_stiffeners = self.superstructures_deckhouses_pressure(zone)
            return superstructure_pressure_plating, superstructure_pressure_stiffeners
        elif zone.zone_index == 5:
            # Mamparos Estancos
            wt_pressure_plating, wt_pressure_stiffeners = self.watertight_bulkheads_pressure()
            return wt_pressure_plating, wt_pressure_stiffeners
        else: # zone.zone_index == 6:
            # Mamparos de colision & Tanques integrales
            intank_pressure_plating, intank_pressure_stiffeners = self.integral_tank_collision_bulkheads_pressure()
            return intank_pressure_plating, intank_pressure_stiffeners

    def design_category_factor_kDC(self) -> float:
        # Mapeo de categoría de diseño a valores de kDC
        kDC_values = {1: 1.0, 2: 0.8, 3: 0.6, 4: 0.4}
        
        # Retornar el valor correspondiente de kDC
        return kDC_values[self.craft.design_cat_index]
    
    def dynamic_load_factor_nCG(self) -> float:
        # Calcular nCG usando la ecuación (1)
        nCG_1 = 0.32 * ((self.craft.LWL / (10 * self.craft.BC)) + 0.084) * (50 - self.craft.B04) * ((self.craft.V**2 * self.craft.BC**2) / self.craft.mLDC)
        
        # Calcular nCG usando la ecuación (2)
        nCG_2 = (0.5 * self.craft.V) / (self.craft.mLDC**0.17)
        
        # Determinar el valor de nCG
        nCG = min(nCG_1, 7) if nCG_1 <= 3 else min(nCG_2, 7)
        
        # Imprimir una advertencia si nCG es mayor que 7 (aunque este caso no debería ocurrir dado el min anterior)
        if nCG > 7:
            print(f"\nCUIDADO: El valor de carga dinámica (nCG)= {nCG} no debería ser mayor a 7, revise sus parámetros iniciales")
        
        return nCG

    def longitudinal_pressure_factor_kL(self, zone, nCG) -> float:
        """
        Parámetros:
            x (float): Posición longitudinal a lo largo de la longitud de la línea de flotación (LWL),
            medida desde el extremo de popa.
        """
        xLWL = zone.x / self.craft.LWL  # Calcula la relación x/LWL
        
        nCG_clamped = min(max(nCG, 3.0), 6.0)  # Limitar nCG entre 3 y 6
        
        kL = ((1 - 0.167 * nCG_clamped) / 0.6) * (xLWL) + (0.167 * nCG_clamped) if xLWL <= 0.6 else 1
                
        return kL

    def area_pressure_factor_kAR(self, zone) -> tuple:
        """
        Calcula el valor de kAR ajustado al material y limitado a un máximo de 1 para Plating y Stiffeners.
        """
        
        # Cálculo de AD para Plating y Stiffeners
        AD_plating = min((zone.l * zone.b) * 1e-6, 2.5 * (zone.b**2) * 1e-6)
        AD_stiffeners = max((zone.lu * zone.s) * 1e-6, 0.33 * (zone.lu**2) * 1e-6)
        
        # Determinación de kR según el tipo de embarcación
        if self.craft.type == 'planning_craft':
            kR_plating = 1
            kR_stiffeners = 1
        else:
            kR_plating = 1.5 - 3e-4 * zone.b
            kR_stiffeners = 1 - 2e-4 * zone.lu
        
        # Cálculo de kAR para Plating
        kAR_plating = (kR_plating * 0.1 * (self.craft.mLDC**0.15)) / (AD_plating**0.3)
        kAR_plating = min(kAR_plating, 1)  # kAR no debe ser mayor que 1
        
        # Cálculo de kAR para Stiffeners
        kAR_stiffeners = (kR_stiffeners * 0.1 * (self.craft.mLDC**0.15)) / (AD_stiffeners**0.3)
        kAR_stiffeners = min(kAR_stiffeners, 1)  # kAR no debe ser mayor que 1
        
        # Ajustes basados en el material
        if self.craft.material == 'Fibra con nucleo (Sandwich)':
            min_kAR = 0.4
        elif self.craft.material == 'Fibra laminada':
            min_kAR = 0.25
        else:
            min_kAR = 0
        
        # Aplicación de los mínimos ajustados según el material
        kAR_plating = max(min_kAR, kAR_plating)
        kAR_stiffeners = max(min_kAR, kAR_stiffeners)
        
        # Retornar ambos valores
        return kAR_plating, kAR_stiffeners
  
    def hull_side_pressure_factor_kZ(self) -> tuple:
        Z = self.craft.Z
        h_plating = val_data("Ingrese la altura del centro del panel por encima de la linea de flotación (metros): ", 0, Z, 0)
        h_stiffeners = val_data("Ingrese la altura del centro del refuerzo por encima de la linea de flotación (metros): ", 0, Z, 0)
        
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
        return 1
 
    #Pressure Zones
    def bottom_pressure(self, zone) -> tuple:
        """
        Calcula la presión de fondo para Plating y Stiffeners, e indica si fue tomada en modo de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de fondo para Plating, Presión de fondo para Stiffeners, Estado de Plating (Desplazamiento/Planeo), Estado de Stiffeners (Desplazamiento/Planeo)
        """
        # Declaramos los factores necesarios para la presión de fondo
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(zone)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL(zone, nCG)
        
        # Se calculan valores base y minimos de la presión de fondo en modo de desplazamiento y planeo
        PBMD_BASE = 2.4 * (self.craft.mLDC**0.33) + 20
        PBMP_BASE = ((0.1 * self.craft.mLDC)/(self.craft.LWL * self.craft.BC))*(1 + (kDC**0.5) * nCG)
        PBM_MIN = 0.45 * (self.craft.mLDC ** 0.33) + (0.9 * self.craft.LWL * kDC)
        
        # Calcula la presión de fondo en modo de desplazamiento
        PBMD_plating = PBMD_BASE * kAR_plating * kDC * kL
        PBMD_stiffeners = PBMD_BASE * kAR_stiffeners * kDC * kL
        
        # Asegúrate de que la presión no sea inferior al mínimo
        PBMD_plating = max(PBM_MIN, PBMD_plating)
        PBMD_stiffeners = max(PBM_MIN, PBMD_stiffeners)

        # Calcula la presión de fondo en modo de planeo
        PBMP_plating = PBMP_BASE * kAR_plating * kL
        PBMP_stiffeners = PBMP_BASE * kAR_stiffeners * kL
        
        # Asegúrate de que la presión no sea inferior al mínimo
        PBMP_plating = max(PBM_MIN, PBMP_plating)
        PBMP_stiffeners = max(PBM_MIN, PBMP_stiffeners)

        # Siempre usa la mayor presión de fondo entre desplazamiento y planeo
        bottom_pressure_plating = max(PBMD_plating, PBMP_plating)
        bottom_pressure_stiffeners = max(PBMD_stiffeners, PBMP_stiffeners)
        
        return bottom_pressure_plating, bottom_pressure_stiffeners

    def side_pressure(self, zone) -> tuple:
        # Declaramos los factores necesarios para la presión de costado
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(zone)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL(zone, nCG)
        kZ_plating, kZ_stiffeners = self.hull_side_pressure_factor_kZ()
        
        # Se calculan valores base y minimos de la presión de costado en modo de desplazamiento y planeo
        PDM_BASE = 0.35 * self.craft.LWL + 14.6
        PBMD_BASE = 2.4 * (self.craft.mLDC**0.33) + 20
        PBMP_BASE = ((0.1 * self.craft.mLDC) / (self.craft.LWL * self.craft.BC)) * (1 +(kDC**0.5) * nCG)
        PSM_MIN = 0.9 * self.craft.LWL * kDC
        
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
        
        # Comparamos PSMD y PSMP y tomamos el mayor
        side_pressure_plating = max(PSMD_plating, PSMP_plating)
        side_pressure_stiffeners = max(PSMD_stiffeners, PSMP_stiffeners)
        
        return side_pressure_plating, side_pressure_stiffeners
    
    def deck_pressure(self, zone):
        # Obtener los factores de ajuste de la presión
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(zone)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL(zone, nCG)
        
        # Valores base para la presión en la cubierta
        PDM_BASE = 0.35 * self.craft.LWL + 14.6
        PDM_MIN = 5  # Presión mínima permitida
        
        # Cálculo de la presión de la cubierta para Plating y Stiffeners
        PDM_plating = PDM_BASE * kAR_plating * kDC * kL
        PDM_stiffeners = PDM_BASE * kAR_stiffeners * kDC * kL
        
        # La presión de cubierta no debe ser inferior al valor mínimo
        deck_pressure_plating = max(PDM_MIN, PDM_plating)
        deck_pressure_stiffeners = max(PDM_MIN, PDM_stiffeners)
        
        return deck_pressure_plating, deck_pressure_stiffeners

    def superstructure_deckhouses_pressure(self, zone):
        # Factores de ajuste de la presión
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(zone)
        kDC = self.design_category_factor_kDC()
        kSUP = self.superstructure_kSUP()  # Factor para superestructuras y casetas
        
        # Valor base de presión para superestructuras y casetas
        PDM_BASE = 0.35 * self.craft.LWL + 14.6
        PDM_MIN = 5  # Presión mínima permitida
        
        # Cálculo de presión para Plating y Stiffeners
        PSUP_plating = PDM_BASE * kDC * kAR_plating * kSUP
        PSUP_stiffeners = PDM_BASE * kDC * kAR_stiffeners * kSUP
        
        # Asegurar que la presión no sea menor al valor mínimo permitido
        superdeck_pressure_plating = max(PDM_MIN, PSUP_plating)
        superdeck_pressure_stiffeners = max(PDM_MIN, PSUP_stiffeners)
        
        return superdeck_pressure_plating, superdeck_pressure_stiffeners
    
    """BULKHEADS"""
    @property
    def hB(self) -> float:
        return val_data("Altura de la columna de agua (metros): ")
    
        # @property
    
    # def get_Db(self) -> float:
    #     return val_data("Profundidad del mamparo (metros): ")
    
    def watertight_bulkheads_pressure(self):
        PWB_plating = PWB_stiffeners = 7 * self.hB
        return PWB_plating, PWB_stiffeners
    
    def integral_tank_collision_bulkheads_pressure(self):
        PTB_plating = PTB_stiffeners = 10 * self.hB
        return PTB_plating, PTB_stiffeners
    
class Plating:
    def __init__(self, craft: object):
        self.craft = craft

    def calculate_plating(self, zone, pressure):
        k2 = self.panel_strength_k2(zone)
        kC = self.curvature_correction_kC(zone)
        
        if self.craft.material in [1, 2]:
            sigma_u = val_data("Esfuerzo ultimo a la tracción (MPa): ")
            sigma_y = val_data("Limite elastico por tracción (MPa): ", 1e-6, sigma_u)
            return max(self.minimum_thickness(zone, sigma_y), self.metal_plating(zone, pressure, k2, kC, sigma_u, sigma_y))
        
        elif self.craft.material == 3:
            sigma_uf = val_data("Resistencia ultima a la flexión (MPa): ")
            return max(self.minimum_thickness(zone, sigma_uf), self.wood_plating(zone, pressure, k2, sigma_uf))
        
        elif self.craft.material == 4:
            # print("\nSeleccione el tipo de fibra de diseño")
            # self.display_menu(self.SKIN_TYPE)
            # choice = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.SKIN_TYPE))
            sigma_uf = val_data("Resistencia ultima a la flexión (MPa): ") 
            return max(self.minimum_thickness(zone, sigma_uf), self.single_skin_plating(zone, pressure, k2, kC, sigma_uf))
        
        else: # self.material == 'Fibra con nucleo (Sandwich)':
            print("\nSeleccione el material del nucleo del sandwich: ")
            available_cores = ('Madera Balsa', 'PVC entrecruzado', 'PVC lineal', 'SAN')
            core_index, core = display_menu(available_cores)
            tau_u = val_data(f"Resistencia última al cortante del núcleo de {core} (MPa): ")
            # k3 = self.panel_stiffness_k3(zone)
            # print("\nSeleccione el tipo de fibra de diseño de la fibra *exterior*")
            # display_menu(self.SKIN_TYPE)
            # choice1 = val_data("Ingrese el número correspondiente: ", 1, len(self.SKIN_TYPE))
            # print("\nSeleccione el tipo de fibra de diseño de la fibra *interior*")
            # display_menu(self.SKIN_TYPE)
            # choice2 = val_data("Ingrese el número correspondiente: ", 1, len(self.SKIN_TYPE))
            # skin_ext = self.SKIN_TYPE[choice1 - 1]
            # skin_int = self.SKIN_TYPE[choice2 - 1]
            return max(self.minimum_thickness(zone, sigma_uf), self.sandwich_plating(zone, pressure, kC, core_index, tau_u))
            
        # if zone.zone_index in [1, 2, 3, 4, 6, 7]:
        #     Logic implemented up 
        # else: # zone.zone_index == 5:
        #     if self.craft.material in [1, 2]:
        #         sigma_u = val_data("Esfuerzo ultimo a la tracción (MPa): ")
        #         sigma_y = val_data("Limite elastico por tracción (MPa): ", 1e-6, sigma_u)
        #         return max(self.minimum_thickness(zone, sigma_y), self.metal_plating(zone, pressure, k2, kC, sigma_u, sigma_y))
            
        #     elif self.craft.material == 3:
        #         Db = val_data("Profundidad del mamparo hasta la cubierta (metros): ")
        #         return 7 * Db
        #     else:
        #         raise Exception("Material no disponible")
        
    def panel_strength_k2(self, zone):
        if self.craft.material == 4:
            return 0.5
        else:
            ar = zone.l / zone.b
            return min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
    
    def panel_stiffness_k3(self, zone):
        ar = zone.l / zone.b
        return min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
        
    def curvature_correction_kC(self, zone):
        cb = zone.c / zone.b
        if cb <= 0.03:
            kC = 1.0
        elif cb <= 0.18 and cb > 0.03: #Ajustado
            kC = 1.1 - (3.33 * self.c) / self.b
        else:  # cb > 0.18
            kC = 0.5
        # Aplica las restricciones de que kC no debe ser menor a 0.5 ni mayor a 1.0
        kC = max(min(kC, 1.0), 0.5)
        return kC
    
    def metal_plating(self, zone, pressure, k2, kC, sigma_u, sigma_y):
        sigma_d = min(0.6 * sigma_u, 0.9 * sigma_y)
        thickness = zone.b * kC * math.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def single_skin_plating(self, zone, pressure, k2, kC, sigma_uf):
        sigma_d = 0.5 * sigma_uf
        thickness = zone.b * kC * math.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def wood_plating(self, zone, pressure, k2, sigma_uf):
        sigma_d = 0.5 * sigma_uf
        thickness = zone.b * math.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def sandwich_plating1(self, pressure, k1, k2, k3, kC):
        sigma_ut = val_data("Resistencia a la tracción de la fibra externa (MPa): ")
        sigma_uc = val_data("Resistencia a la compresión de la fibra interna (MPa): ")
        Ei = val_data("Módulo de elasticidad de la fibra interna (MPa): ")
        Eo = val_data("Módulo de elasticidad de la fibra externa (MPa): ")
        tau_u = val_data("Resistencia última al cortante del núcleo (MPa): ")
        Eio = (Ei + Eo) / 2
        #sigma_ub = val_data("Menor de las resistencias a la tracción o a la compresión (MPa): ")
        
        #Design stresses for the inner and outer skin of the sandwich [N/mm2]:
        sigma_dt = 0.5 * sigma_ut
        sigma_dc = 0.5 * sigma_uc
        
        #Minimum required section modulus of the inner/outter skin of sandwich 1 cm wide [cm3/cm]:
        SM_inner = ((self.b**0.5) * (kC**0.5) * pressure * k2)/(6e5 * sigma_dt)
        SM_outter = ((self.b**0.5) * (kC**0.5) * pressure * k2)/(6e5 * sigma_dc)   
        
        #Minimum required section modulus of the sandwich 1 cm wide [cm4/cm]:
        second_I = ((self.b**3) * (kC**3) * pressure * k3) / (12e6 * k1 * Eio)
        
        # Shear strength aspect ratio factor kSHC
        lb = self.l / self.b
        kSHC = 0.035 + 0.394 * lb - 0.09 * lb**2 if lb < 2 else 0.5
        
        print("\nSeleccione el material del nucleo del sandwich: ")
        core_materials_options = ('Madera Balsa', 'PVC entrecruzado', 'PVC lineal', 'SAN')
        core_material = display_menu(core_materials_options)

        if core_material == 1:
            tau_d = tau_u * 0.5
        elif core_material == 2:
            tau_d = tau_u * 0.55
        elif core_material == 3:
            tau_d = tau_u * 0.65
        else: #core_material == 4:
            tau_d = tau_u * 0.5
            
        #Minimum design core shear according to craft length
        if self.craft.LH < 10:
            tau_d = max(tau_d, 0.25)
        elif self.craft.LH <= 10 and self.craft.LH <= 15:
            tau_d = max(tau_d, 0.25 + 0.03 * (self.craft.LH - 10))
        else:
            tau_d = max(tau_d, 0.40)
        
        #Thickness required by shear load capabilities:
        thickness = (kC**0.5) * ((kSHC * pressure * self.b)/(1000 * tau_d))
    
        #sandwich thickness = tc + 0.5 (t i + to) is the distance between mid-thickness of the skins of the sandwich, in milimetres
        
        return SM_inner, SM_outter, second_I, thickness
    
    def sandwich_plating(self, zone, pressure, kC, core_index, tau_u):
        # 1. Relación de aspecto (l/b) y factor kSHC
        lb = zone.l / zone.b
        kSHC = 0.035 + 0.394 * lb - 0.09 * lb**2 if lb < 2 else 0.5
        # 2. Reducción del esfuerzo último según tipo de núcleo
        core_factors = {1: 0.50, 2: 0.55, 3: 0.65, 4: 0.50}
        tau_d = tau_u * core_factors.get(core_index)
        # 3. Esfuerzo mínimo según eslora (LH)
        if self.craft.LH < 10:
            tau_min = 0.25
        elif 10 <= self.craft.LH <= 15:
            tau_min = 0.25 + 0.03 * (self.craft.LH - 10)
        else:
            tau_min = 0.40
        tau_d = max(tau_d, tau_min)
        # 4. Cálculo final del espesor del núcleo
        sandwich_thickness = (kC ** 0.5) * ((kSHC * pressure * zone.b) / (1000 * tau_d)) #distance between mid-thickness of the skins of the sandwich
        return sandwich_thickness
    
    def wash_plates_plating(self):
        return None
    
    def watertight_bulkheads_plating(self):
        return None

    def minimum_thickness(self, zone, sigma):
        if self.craft.material == 1:
            A = 1
            k5 = math.sqrt(240/sigma)
            k7 = 0.015 if zone.zone_index == 1 else 0
            k8 = 0.08
            return k5 * (A + k7 * self.craft.V + k8 * pow(self.craft.mLDC, 0.33)) if zone.zone_index in [1, 2] else 1.5 + 0.07 * self.craft.LWL
        elif self.craft.material == 2:
            A = 1
            k5 = math.sqrt(125/sigma)
            k7 = 0.02 if zone.zone_index == 1 else 0
            k8 = 0.1
            return k5 * (A + k7 * self.craft.V + k8 * pow(self.craft.mLDC, 0.33)) if zone.zone_index in [1, 2] else 1.35 + 0.06 * self.craft.LWL
        elif self.craft.material == 3:
            A = 3
            k5 = math.sqrt(30/sigma)
            k7 = 0.05 if zone.zone_index == 1 else 0
            k8 = 0.3      
            return k5 * (A + k7 * self.craft.V + k8 * pow(self.craft.mLDC, 0.33)) if zone.zone_index in [1, 2] else 3.8 + 0.17 * self.craft.LWL
        else: #self.craft.material in [3, 4]:
            k5 = 1 #Corregir por tipo de fibra
            k7 = 0.03 if zone.zone_index == 1 else 0
            k8 = 0.15
            return 0.43  * k5 * (A + k7 * self.craft.V + k8 * pow(self.craft.mLDC, 0.33)) if zone.zone_index in [1, 2] else k5 * (1.45 + 0.14 * self.craft.LWL)

def main():
    print("\nESCANTILLONADO ISO 12215-5 - ISO 12215-5 SCANTLINGS\n*Para embarcaciones entre los 2.5 y 24 m de eslora*\n")
    # designer = input("Diseñador: ") #Son necesarios estos inputs ahora?
    # boat = input("Embarcación: ")
    # company = input("Empresa: ")
    # management = input("Gerencia: ")
    # division = input("División: ")
    # values = {} # Diccionario pensado para almacenar los valores
    
    print("\nSeleccione la categoría de diseño de su embarcación")
    categories = ('A (“Oceano”)', 'B ("Offshore")', 'C ("Costera")', 'D ("Aguas calmadas")')
    design_cat_index, design_cat = display_menu(categories)
    
    print("\nSeleccione el material de su embarcación")
    available_materials = ('Acero', 'Aluminio', 'Madera laminada o contrachapada', 'Fibra laminada', 'Fibra con nucleo (Sandwich)')
    material_index, material = display_menu(available_materials)
    
    # Instanciar las clases estáticas
    craft = Craft(design_cat_index, material_index)
    pressure = Pressures(craft)
    plating = Plating(craft)
    
    # Determinar las zonas disponibles según el material
    #available_zones = list(range(1, 4)) if material_index not in [1, 2] else list(range(1, 8))
    
    while True:
        print("\nSeleccione la zona que desea escantillonar: ")
        #zone_index, zone_name = display_menu([list(craft.ZONE_DIM.keys())[i - 1] for i in available_zones])
        zone_index, zone_name = display_menu(list(craft.ZONE_DIM.keys()))
        
        try:
            zone = Zone(craft, zone_name, zone_index)
            print(f"\nAtributos definidos para la zona {zone_name}:", zone.zone_attributes)
            
            # Calcular presión
            zone_pressure = pressure.calculate_pressure(zone)
            print(f"\nPresión calculada para la zona '{zone_name}': Forro exterior = {zone_pressure[0]:.2f} MPa, Refuerzos = {zone_pressure[1]:.2f} MPa")
            
            # Calcular espesor
            thickness = plating.calculate_plating(zone, zone_pressure[0])
            print(f"\nEspesor mínimo requerido para la zona '{zone_name}' = {thickness:.2f} mm")
            
            #values[zone_name] = thickness
            
        except ValueError as e:
            print(f"Error: {e}")

        program_continue = val_data("\nIngrese 1 para escantillonar otra zona o 0 para salir: " , 0, 1, 0)
        if program_continue == 0:
            print("\nPrograma finalizado.")
            break
        
def display_menu(items):
    """
    Muestra un menú enumerado basado en una lista de elementos y devuelve
    el índice seleccionado y el elemento correspondiente.

    Args:
        items (list): Lista de elementos a mostrar en el menú.

    Returns:
        tuple: Índice seleccionado (0-indexed) y el elemento correspondiente, o (None, None) si el usuario selecciona 0.
    """
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")

    # Solicitar entrada del usuario
    choice = val_data("Ingrese el número correspondiente: ", 1, len(items), None, False)

    # Manejar la opción de salir
    if choice == 0:
        return None, None

    # Retornar el índice y el elemento correspondiente
    return choice, items[choice - 1]

if __name__ == "__main__":
    main()
