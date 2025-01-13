import numpy as np
from validations import val_data

class Craft:
    def __init__(self, designer, boat, company, management, division, design_cat, material, zone_name, zone_index):
        self.designer = designer
        self.boat = boat
        self.company = company
        self.management = management
        self.division = division
        self.design_cat = design_cat
        self.material = material
        self.zone_name = zone_name
        self.zone_index = zone_index
        
        # Principal Craft Data
        print("\nIngrese los atributos principales de la embarcación")
        self.LH = val_data("Eslora del casco (metros): ", True, True, -1, 2.5, 24)
        self.LWL = val_data("Eslora de flotación (metros): ", True, True, -1, 0, self.LH)
        self.BH = val_data("Manga del casco (metros): ")
        self.BWL = val_data("Manga de flotación (metros): ", True, True, -1, 0, self.BH)
        self.BC = val_data(f"Manga entre pantoques ('Chine beam') a {0.4 * self.LWL} metros de la popa (metros): ", True, True, -1, 0, self.BH)
        self.mLDC = val_data("Desplazamiento de la embarcación (toneladas): ") / 1000
        self.V = self.get_V()
        self.B04 = self.get_B04()
        self.Z = val_data("Altura de francobordo (metros): ")
        self.type = self.get_craft_type()
        
        # Diccionario de zonas y sus atributos necesarios
        self.zones_data = {
            'Casco de Fondo': ['b', 'l', 's', 'lu', 'c', 'x'],
            'Casco de Costado': ['b', 'l', 's', 'lu', 'c'],
            'Espejo de Popa': ['b', 'l', 's', 'lu'],
            'Cubierta de Principal': ['b', 'l', 'c'],
            'Cubiertas Inferiores/Otras Cubiertas': ['b', 'l', 'c'],
            'Cubiertas Humedas': ['b', 'l', 'c'],
            'Cubiertas de Superestructura y Casetas de Cubierta': ['b', 'l'],
            'Mamparos Estancos': ['b', 'l', 'hB'],
            'Mamparos de Tanques Profundos': ['b', 'l', 'hB'],
            'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos': ['b', 'l'],
            'Túneles de Waterjets': ['b', 'l'],
            'Túneles de Bow Thrusters': ['b', 'l'],
            'Cubiertas de Operación o Almacenamiento de Vehículos': ['b', 'l', 'c'],
        }
      
    def get_V(self) -> float:
        min_speed = 2.26 * np.sqrt(self.LWL)
        return val_data(f"Velocidad máxima (nudos, debe ser >= {min_speed:.2f}): ", True, True, -1, min_speed)

    def get_B04(self) -> float:
        B04 = val_data(f"Ángulo de astilla muerta de fondo a {0.4 * self.LWL:.2f} metros de la popa (°grados): ")
        if B04 < 10 or B04 > 30:
            print(f"Advertencia: El ángulo de astilla muerta {B04}° está fuera del rango sugerido (10° a 30°).")
        return B04
        
    @property
    def get_Db(self) -> float:
        return val_data("Profundidad del mamparo (metros): ")
    
    @property
    def get_hB(self) -> float:
        return val_data("Altura de la columna de agua (metros): ")
    
    def get_craft_type(self) -> str:
        # Determinar el tipo de embarcación basado en la relación V/LWL
        if self.V / np.sqrt(self.LWL) >= 5:
            return "planning_craft"
        else: # V / LWL < 5
            return "displacement_craft"
        
    """PANEL/STIFFENER DIMENSIONS"""
    # Definir las zonas y sus atributos dependientes
    def get_zone_data(self, zone_name) -> dict:
        
        # Diccionario de funciones para solicitar cada atributo
        attribute_prompts = {
            'l': lambda: val_data(f"l: Longitud más larga de los paneles de la zona {zone_name} (mm): "),
            'b': lambda: val_data(f"b: Longitud más corta de los paneles de la zona {zone_name} (mm): ", True, True, -1, 0, zone_attributes.get('l', float('inf'))),
            'lu': lambda: val_data(f"lu: Luz o espacio entre refuerzos de la zona {zone_name} (mm): ", True, True, 0),
            's': lambda: val_data(f"s: Separación del alma o viga longitudinal de la zona {zone_name} (mm): "),
            'c': lambda: val_data(f"c: Corona o curvatura del panel/refuerzo de la zona {zone_name} (mm): "),
            'x': lambda: val_data(f"x: Distancia longitudinal desde popa hasta el punto de análisis de la zona {zone_name} (metros): ", True, True, self.LH, 0, self.LH),
            'hB': lambda: val_data(f"hB: Altura de la columna de agua en la zona {zone_name} (mm): "),
        }

        # Obtener los atributos necesarios para la zona seleccionada
        required_attributes = self.zones_data[zone_name]
        
        # Diccionario para almacenar los valores ingresados
        zone_attributes = {}
        
        # Recolectar los valores dinámicamente
        for attribute in required_attributes:
            zone_attributes[attribute] = attribute_prompts[attribute]()  # Llama a la función `lambda`

        return zone_attributes
    
class Pressures:
    
    def __init__(self, craft: object, zone_attributes: dict):
        self.craft = craft
        # Extraer los valores del diccionario de forma segura
        self.b = zone_attributes.get('b', None)
        self.l = zone_attributes.get('l', None)
        self.s = zone_attributes.get('s', None)
        self.lu = zone_attributes.get('lu', None)
        self.c = zone_attributes.get('c', None)
        self.x = zone_attributes.get('x', None)
        self.hB = zone_attributes.get('hB', None)
        
        
    def calculate_pressure(self):
        print(f"Zone index: {self.craft.zone_index}")
        if self.craft.zone_index == 1:
            bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.bottom_pressure()
            return bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners
        elif self.craft.zone_index == 2:
            pressure, index = self.side_pressure()
            return pressure, index
        elif self.craft.zone_index == 3:
            pressure, index = self.deck_pressure()
            return pressure, index
        elif self.craft.zone_index == 4:
            pressure = self.superstructures_deckhouses_pressure()
            return pressure, 0
        elif self.craft.zone_index == 5:
            pressure = self.watertight_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone_index == 6:
            pressure = self.integral_tank_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone_index == 7:
            pressure = self.wash_plates_pressure()
            return pressure, 0
        elif self.craft.zone_index == 8:
            pressure = self.collision_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone_index == 9:
            pressure = self.nonwatertight_partial_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone_index == 10:
            pressure = self.transmission_pillar_loads_pressure()
            return pressure, 0
        else:
            return "La zona escogida no se encuentra disponible"

    def design_category_factor_kDC(self) -> float:        
        # Mapeo de categoría de diseño a valores de kDC
        kDC_values = {'A (“Oceano”)': 1.0, 'B ("Offshore")': 0.8, 'C ("Costera")': 0.6, 'D ("Aguas calmadas")': 0.4}
        
        # Retornar el valor correspondiente de kDC
        return kDC_values[self.craft.design_cat]
    
    def dynamic_load_factor_nCG(self) -> float:
        """
        Calcula el factor de carga dinámica nCG para embarcaciones de motor en modo de planeo.
        Retorna:
        float: El valor de nCG, limitado a un máximo de 7.
        """

        # Calcular nCG usando la ecuación (1)
        nCG_1 = 0.32 * ((self.craft.LWL / (10 * self.craft.BC)) + 0.084) * (50 - self.craft.B04) * ((self.craft.V**2 * self.craft.BC**2) / self.craft.mLDC)
        
        # Calcular nCG usando la ecuación (2)
        nCG_2 = (0.5 * self.craft.V) / (self.craft.mLDC**0.17)
        
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

    def longitudinal_pressure_factor_kL(self) -> float:
        """
        Parámetros:
            x (float): Posición longitudinal a lo largo de la longitud de la línea de flotación (LWL),
            medida desde el extremo de popa.
        """
        xLWL = self.x / self.craft.LWL  # Calcula la relación x/LWL
        
        if xLWL > 0.6:
            kL = 1.0  # Si x/LWL es mayor que 0.6, kL es 1.0
        else:
            nCG = self.dynamic_load_factor_nCG()  # Calcular nCG
            nCG_clamped = min(max(nCG, 3.0), 6.0)  # Limitar nCG entre 3 y 6
            
            # Aplica la ecuación para valores de x/LWL <= 0.6
            kL = ((1 - 0.167 * nCG_clamped) * (xLWL / 0.6)) + (0.167 * nCG_clamped)
            kL = min(kL, 1.0)  # Asegurarse de que kL no sea mayor que 1.0
        
        return kL

    def area_pressure_factor_kAR(self) -> tuple:
        """
        Calcula el valor de kAR ajustado al material y limitado a un máximo de 1 para Plating y Stiffeners.
        """
        
        # Cálculo de AD para Plating y Stiffeners
        AD_plating = min((self.l * self.b) * 1e-6, 2.5 * (self.b**2) * 1e-6)
        AD_stiffeners = max((self.lu * self.s) * 1e-6, 0.33 * (self.lu**2) * 1e-6)
        
        # Determinación de kR según el tipo de embarcación
        if self.craft.type == 'planning_craft':
            kR_plating = 1
            kR_stiffeners = 1
        else:
            kR_plating = 1.5 - 3e-4 * self.b
            kR_stiffeners = 1 - 2e-4 * self.lu
        
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
    def bottom_pressure(self) -> tuple:
        """
        Calcula la presión de fondo para Plating y Stiffeners, e indica si fue tomada en modo de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de fondo para Plating, Presión de fondo para Stiffeners, Estado de Plating (Desplazamiento/Planeo), Estado de Stiffeners (Desplazamiento/Planeo)
        """
        # Declaramos los factores necesarios para la presión de fondo
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR()
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL()
        
        # Se calculan valores base y minimos de la presión de fondo en modo de desplazamiento y planeo
        PBMD_BASE = 2.4 * (self.craft.mLDC**0.33) + 20
        PBMP_BASE = ((0.1 * self.craft.mLDC)/(self.craft.LWL * self.craft.BC))*((1 + kDC**0.5) * nCG)
        PBM_MIN = 0.45 * (self.craft.mLDC ** 0.33) + (0.9 * self.craft.LWL * kDC)
        
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

    def side_pressure(self) -> tuple:
        """
        Calcula la presión de costado para Plating y Stiffeners según las categorías de diseño y modos de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de costado para Plating, Presión de costado para Stiffeners.
        """
        
        # Declaramos los factores necesarios para la presión de costado
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR()
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL()
        kZ_plating, kZ_stiffeners = self.hull_side_pressure_factor_kZ()
        
        # Se calculan valores base y minimos de la presión de costado en modo de desplazamiento y planeo
        PDM_BASE = 0.35 * self.craft.LWL + 14.6
        PBMD_BASE = 2.4 * (self.craft.mLDC**0.33) + 20
        PBMP_BASE = ((0.1 * self.craft.mLDC) / (self.craft.LWL * self.craft.BC)) * ((1 + kDC**0.5) * nCG)
        PSM_MIN = 0.9 * self.craft.LWL * kDC
        
        # Categorías A y B: Comparamos PSMD y PSMP y tomamos el mayor
        if self.craft.design_cat in ['A', 'B']:
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
            bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.bottom_pressure()
            
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
    
    def deck_pressure(self):
        """
        Calcula la presión sobre la cubierta para Plating y Stiffeners.
        Retorna:
            tuple: Presión sobre la cubierta para Plating y Stiffeners, asegurando que no sea inferior a un valor mínimo.
        """
        # Obtener los factores de ajuste de la presión
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR()
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_distribution_kL()
        
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

    def superstructure_deckhouses_pressure(self):
        """
        Calcula la presión sobre las superestructuras y casetas de cubierta para Plating y Stiffeners.
        Retorna:
            tuple: Presión sobre las superestructuras y casetas de cubierta para Plating y Stiffeners.
        """
        # Factores de ajuste de la presión
        kDC = self.design_category_factor_kDC()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR()
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
    
    def watertight_bulkheads_pressure(self): #Pasar hB mediante el main
        """ Presión para mamparos estancos. """
        PWB = 7 * self.hB
        return PWB
    
    def integral_tank_bulkheads_pressure(self):
        """ Presión para mamparos de tanques integrales. """
        PTB = 10 * self.hB
        return PTB

class Plating:
    def __init__(self, craft: object, zone_attributes: dict):
        self.craft = craft
        self.b = zone_attributes.get('b', None)
        self.l = zone_attributes.get('l', None)
        self.s = zone_attributes.get('s', None)
        self.lu = zone_attributes.get('lu', None)
        self.c = zone_attributes.get('c', None)
        self.x = zone_attributes.get('x', None)
        self.hB = zone_attributes.get('hB', None)

    def calculate_plating(self, pressure):
        k1 = 0.017
        k2 = self.panel_strength_k2()
        kC = self.curvature_correction_kC()
        
        if self.craft.zone_index in [1, 2, 3, 4, 5]:
            if self.craft.material in [1, 2]:
                return self.metal_plating(pressure, k2, kC)
            elif self.craft.material == 3:
                thickness = self.single_skin_plating(pressure, k2, kC)
                return thickness
            elif self.craft.material == 4:
                return self.wood_plating(pressure, k2)
            elif self.craft.material == 5:
                k3 = self.panel_stiffness_k3()
                return self.fiber_core_plating(pressure, k2, k3, kC)
        else:
            # 'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos': ['b', 'l'],
            # 'Túneles de Waterjets': ['b', 'l'],
            # 'Túneles de Bow Thrusters': ['b', 'l'],
            # 'Cubiertas de Operación o Almacenamiento de Vehículos': ['b', 'l', 'c']
            if self.craft.zone_index == 8:
                thickness = self.bulkhead_scantling()
                return thickness
            elif self.craft.zone_index == 9:
                thickness = self.tank_scantling()
                return thickness
            elif self.craft.zone_index == 10:
                thickness = 0
                return thickness
            elif self.craft.zone_index == 11:
                thickness = 0
                return thickness
            elif self.craft.zone_index == 12:
                thickness = 0
                return thickness
            
    def panel_strength_k2(self):
        if self.craft.material == 4:
            return 0.5
        else:
            ar = self.l / self.b
            return min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
    
    def panel_stiffness_k3(self):
        ar = self.l / self.b
        return min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
        
    def curvature_correction_kC(self):
        cb = self.c / self.b
        if cb <= 0.03:
            kC = 1.0
        elif cb <= 0.18 and cb > 0.03: #Ajustado
            kC = 1.1 - (3.33 * self.c) / self.b
        else:  # cb > 0.18
            kC = 0.5
        # Aplica las restricciones de que kC no debe ser menor a 0.5 ni mayor a 1.0
        kC = max(min(kC, 1.0), 0.5)
        return kC
    
    def metal_plating(self, pressure, k2, kC):
        sigma_u = val_data("Esfuerzo ultimo a la tracción del material (MPa): ")
        sigma_y = val_data("Limite elastico por tracción del material (MPa): ")
        sigma_d = min(0.6 * sigma_u, 0.9 * sigma_y)
        thickness = self.b * kC * np.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def single_skin_plating(self, pressure, k2, kC):
        sigma_uf = val_data("Resistencia ultima a la flexión (MPa): ")
        sigma_d = 0.5 * sigma_uf
        thickness = self.b * kC * np.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def wood_plating(self, pressure, k2):
        sigma_uf = val_data("Resistencia ultima a la flexión (MPa): ")
        sigma_d = 0.5 * sigma_uf
        thickness = self.b * np.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def fiber_core_plating(self, pressure):
        sigma_uo = val_data("Resistencia a la tracción de la fibra externa (MPa): ")
        sigma_ui = val_data("Resistencia a la tracción de la fibra interna (MPa): ")
        sigma_ub = val_data("Menor de las resistencias a la tracción o a la compresión (MPa): ")
        return None
    
    def wash_plates_plating(self):
        return None
    
    def watertight_bulkheads_plating(self):
        return None

def main():
    print("ESCANTILLONADO ISO 12215-5 - ISO 12215-5 SCANTLINGS\n")
    designer = input("Diseñador: ")
    boat = input("Embarcación: ")
    company = input("Empresa: ")
    management = input("Gerencia: ")
    division = input("División: ")
    values = {}
    
    print("\nSeleccione la categoría de diseño de su embarcación")
    categories = ('A (“Oceano”)', 'B ("Offshore")', 'C ("Costera")', 'D ("Aguas calmadas")')
    design_cat_index, design_cat = display_menu(categories)
    
    print("\nSeleccione el material de su embarcación")
    available_materials = ('Acero', 'Aluminio', 'Fibra laminada', 'Madera laminada o contrachapada', 'Fibra con nucleo (Sandwich)')
    material_index, material = display_menu(available_materials)
    
    craft = Craft(designer, boat, company, management, division, design_cat, material_index, zone_name=None, zone_index=None)
    
    # Determinar las zonas disponibles según el material
    available_zones = list(range(1, 12)) if material_index not in [1, 2] else list(range(1, 14))
    
    while True:
        print("\nSeleccione la zona que desea escantillonar:\n(Ingrese 0 para finalizar el programa)")
        zone_index, zone_name = display_menu([list(craft.zones_data.keys())[i - 1] for i in available_zones])
        
        if zone_index is None:
            print("\nPrograma finalizado.")
            break
        
        try:
            # Actualizar la zona en Craft
            craft.zone_index = zone_index
            craft.zone_name = zone_name
                    
            # Obtener datos de la zona
            zone_attributes = craft.get_zone_data(zone_name)
            print("\nAtributos definidos para la zona:", zone_attributes)
            
            # Instanciar las clases con los datos de la zona seleccionada
            pressure = Pressures(craft, zone_attributes)
            plating = Plating(craft, zone_attributes)
            
            # Calcular presión
            zone_pressure = pressure.calculate_pressure()
            print(f"\nPresión calculada para la zona '{zone_name}': {zone_pressure:.3f} MPa")
            
            # Calcular espesor
            thickness = plating.calculate_plating(zone_pressure)
            print(f"\nEl espesor mínimo requerido para la zona '{zone_name}': {thickness:.3f} mm")
            
            #values[zone_name] = thickness
            
        except ValueError as e:
            print(f"Error: {e}")

def display_menu(items):
    """
    Muestra un menú enumerado basado en una lista de elementos y devuelve
    el índice seleccionado y el elemento correspondiente.

    Args:
        items (list): Lista de elementos a mostrar en el menú.

    Returns:
        tuple: Índice seleccionado (0-indexed) y el elemento correspondiente, o (None, None) si el usuario selecciona 0.
    """
    # Mostrar el menú enumerado
    print("\nSeleccione una opción:")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")

    # Solicitar entrada del usuario
    choice = val_data("Ingrese el número correspondiente (o 0 para salir): ", False, True, 0, 0, len(items))

    # Manejar la opción de salir
    if choice == 0:
        return None, None

    # Retornar el índice y el elemento correspondiente
    return choice, items[choice - 1]

if __name__ == "__main__":
    main()
