"""
    Main de la calculadora de ISO 12215-5
"""

import numpy as np
from validations import val_data

class Craft:
    def __init__(self, designer, boat, company, management, division, design_cat, material, zone_name, zone):
        self.values = {}
        self.designer = designer
        self.boat = boat
        self.company = company
        self.management = management
        self.division = division
        self.design_cat = design_cat
        self.material = material
        self.zone_name = zone_name
        self.zone = zone
        
    #Metodo para pedir datos y validar si ya existe
    def get_value(self, key, prompt, *args) -> float:
        if key not in self.values:
            self.values[key] = val_data(prompt, *args)
        return self.values[key]
    
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
        h13_values = {1: 4, 2: 2.5, 3: 0.5, 4: 4}
        h13 = max(h13_values.get(self.design_cat), (L / 12))
        return h13
    
    def get_sigma_y(self) -> float:
        return self.get_value('sigma_y', "Limite elastico por tracción del material (MPa): ")
    
    def get_sigma_u(self) -> float:
        return self.get_value('sigma_u', "Esfuerzo ultimo a la tracción del material (MPa): ")
    
    def get_sigma_uf(self) -> float:
        return self.get_value('sigma_uf', "Resistencia ultima a la flexión (MPa): ")
    
    def get_sigma_uo(self) -> float:
        return self.get_value('sigma_uo', "Resistencia a la tracción de la fibra externa (MPa): ")
    
    def get_sigma_ui(self) -> float:
        return self.get_value('sigma_ui', "Resistencia a la tracción de la fibra interna (MPa): ")
    
    def get_sigma_ub(self) -> float:
        return self.get_value('sigma_ub', "Menor de las resistencias a la tracción o a la compresión (MPa): ")
    
    def get_b(self) -> float:
        return val_data(f"Longitud mas corta de los paneles de la zona {self.zone} (mm): ")
    
    def get_l(self) -> float:
        #b = self.get_b(zone) #Revisar esto porque si no se guarda en diccionario se volveria a pedir b innecesariamente
        return val_data(f"Longitud mas larga de los paneles de la zona {self.zone} (mm): ", True, True, 0)
    
    def get_s(self) -> float:
        return val_data(f"Separación del alma o viga longitudinal, rigidizador, transversal, etc. de la zona: {self.zone} (metros): ")
    
    def get_lu(self) -> float:
        #s = self.get_s(zone)
        return val_data(f"Luz o espacio entre refuerzos de la zona {self.zone} (mm): ", True, True, 0) #Longitud del alma longitudinal, rigidizador, transversal o viga
    
    def get_c(self) -> float:
        return val_data(f"Corona o curvatura del panel/refuerzo de la zona {self.zone} (mm): ")
    
    def get_x(self) -> float:
        LH = self.get_LH()
        return val_data(f"Distancia longitudinal desde popa hasta el punto de analisis de {self.zone} (metros): ", True, True, LH, 0)
    
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
        if self.craft.zone == 1:
            bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.bottom_pressure()
            return bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners
        elif self.craft.zone == 2:
            pressure, index = self.side_pressure()
            return pressure, index
        elif self.craft.zone == 3:
            pressure, index = self.deck_pressure()
            return pressure, index
        elif self.craft.zone == 4:
            pressure = self.superstructures_deckhouses_pressure()
            return pressure, 0
        elif self.craft.zone == 5:
            pressure = self.watertight_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone == 6:
            pressure = self.integral_tank_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone == 7:
            pressure = self.wash_plates_pressure()
            return pressure, 0
        elif self.craft.zone == 8:
            pressure = self.collision_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone == 9:
            pressure = self.nonwatertight_partial_bulkheads_pressure()
            return pressure, 0
        elif self.craft.zone == 10:
            pressure = self.transmission_pillar_loads_pressure()
            return pressure, 0
        else:
            return "La zona escogida no se encuentra disponible"

    def design_category_factor_kDC(self) -> float:        
        # Mapeo de categoría de diseño a valores de kDC
        kDC_values = {'A': 1.0, 'B': 0.8, 'C': 0.6, 'D': 0.4}
        
        # Retornar el valor correspondiente de kDC
        return kDC_values[self.craft.design_cat]
    
    def dynamic_load_factor_nCG(self) -> float:
        """
        Calcula el factor de carga dinámica nCG para embarcaciones de motor en modo de planeo.
        Retorna:
        float: El valor de nCG, limitado a un máximo de 7.
        """

        # Calcular nCG usando la ecuación (1)
        nCG_1 = 0.32 * ((self.craft.get_LWL() / (10 * self.craft.get_BC())) + 0.084) * (50 - self.craft.get_B04()) * ((self.craft.get_V()**2 * self.craft.get_BC()**2) / self.craft.get_mLDC())
        
        # Calcular nCG usando la ecuación (2)
        nCG_2 = (0.5 * self.craft.get_V()) / (self.craft.get_mLDC()**0.17)
        
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

    def longitudinal_pressure_factor_kL(self, LWL) -> float:
        """
        Parámetros:
            x (float): Posición longitudinal a lo largo de la longitud de la línea de flotación (LWL),
            medida desde el extremo de popa.
        """
        xLWL = self.x / LWL  # Calcula la relación x/LWL
        
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
        craft_type = self.craft.get_craft_type()  # Tipo de embarcación
        
        # Cálculo de AD para Plating y Stiffeners
        AD_plating = min((self.l * self.b) * 1e-6, 2.5 * (self.b**2) * 1e-6)
        AD_stiffeners = max((self.lu * self.s) * 1e-6, 0.33 * (self.lu**2) * 1e-6)
        
        # Determinación de kR según el tipo de embarcación
        if craft_type == 'planning_craft':
            kR_plating = 1
            kR_stiffeners = 1
        else:
            kR_plating = 1.5 - 3e-4 * self.b
            kR_stiffeners = 1 - 2e-4 * self.lu
        
        # Cálculo de kAR para Plating
        kAR_plating = (kR_plating * 0.1 * (self.craft.get_mLDC()**0.15)) / (AD_plating**0.3)
        kAR_plating = min(kAR_plating, 1)  # kAR no debe ser mayor que 1
        
        # Cálculo de kAR para Stiffeners
        kAR_stiffeners = (kR_stiffeners * 0.1 * (self.craft.get_mLDC()**0.15)) / (AD_stiffeners**0.3)
        kAR_stiffeners = min(kAR_stiffeners, 1)  # kAR no debe ser mayor que 1
        
        # Ajustes basados en el material
        if self.material == 'Fibra con nucleo (Sandwich)':
            min_kAR = 0.4
        elif self.material == 'Fibra laminada':
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
    def bottom_pressure(self, material, LWL, BC, mLDC, V, B04) -> tuple:
        """
        Calcula la presión de fondo para Plating y Stiffeners, e indica si fue tomada en modo de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de fondo para Plating, Presión de fondo para Stiffeners, Estado de Plating (Desplazamiento/Planeo), Estado de Stiffeners (Desplazamiento/Planeo)
        """
        # Declaramos los factores necesarios para la presión de fondo
        nCG = self.dynamic_load_factor_nCG(LWL, BC, mLDC, V, B04)
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR(material, mLDC)
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL(LWL, BC, mLDC, V, B04)
        
        # Se calculan valores base y minimos de la presión de fondo en modo de desplazamiento y planeo
        PBMD_BASE = 2.4 * (self.craft.get_mLDC()**0.33) + 20
        PBMP_BASE = ((0.1 * self.craft.get_mLDC())/(self.craft.get_LWL() * self.craft.get_BC()))*((1 + kDC**0.5) * nCG)
        PBM_MIN = 0.45 * (self.craft.get_mLDC() ** 0.33) + (0.9 * self.craft.get_LWL() * kDC)
        
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

    def side_pressure(self, LWL, BC, mLDC) -> tuple:
        """
        Calcula la presión de costado para Plating y Stiffeners según las categorías de diseño y modos de planeo o desplazamiento.
        
        Retorna:
            tuple: Presión de costado para Plating, Presión de costado para Stiffeners.
        """
        design_category = self.craft.get_design_category()
        
        # Declaramos los factores necesarios para la presión de costado
        nCG = self.dynamic_load_factor_nCG()
        kAR_plating, kAR_stiffeners = self.area_pressure_factor_kAR()
        kDC = self.design_category_factor_kDC()
        kL = self.longitudinal_pressure_factor_kL()
        kZ_plating, kZ_stiffeners = self.hull_side_pressure_factor_kZ()
        
        # Se calculan valores base y minimos de la presión de costado en modo de desplazamiento y planeo
        PDM_BASE = 0.35 * self.craft.get_LWL() + 14.6
        PBMD_BASE = 2.4 * (self.craft.get_mLDC()**0.33) + 20
        PBMP_BASE = ((0.1 * self.craft.get_mLDC()) / (self.craft.get_LWL() * self.craft.get_BC())) * ((1 + kDC**0.5) * nCG)
        PSM_MIN = 0.9 * self.craft.get_LWL() * kDC
        
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
            bottom_pressure_plating, bottom_pressure_stiffeners, index_plating, index_stiffeners = self.bottom_pressure(LWL, BC, mLDC)
            
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
        PDM_BASE = 0.35 * self.craft.get_LWL() + 14.6
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
        PDM_BASE = 0.35 * self.craft.get_LWL() + 14.6
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

    def calculate_plating(self, pressure):
        k1 = 0.017
        k2 = self.panel_strength_k2()
        kC = self.curvature_correction_kC()
        
        if self.craft.zone in [1, 2, 3, 4, 5]:
            if self.craft.material == 1:
                return self.steel_thickness(pressure, k2, kC)
            elif self.craft.material == 2:
                return self.aluminum_thickness(pressure, k2, kC)
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
            if self.craft.zone == 8:
                thickness = self.bulkhead_scantling()
                return thickness
            elif self.craft.zone == 9:
                thickness = self.tank_scantling()
                return thickness
            elif self.craft.zone == 10:
                thickness = 0
                return thickness
            elif self.craft.zone == 11:
                thickness = 0
                return thickness
            elif self.craft.zone == 12:
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
    
    def steel_thickness(self, pressure, k2, kC):
        sigma_u = self.craft.get_sigma_u()
        sigma_y = self.craft.get_sigma_y()
        sigma_d = min(0.6 * sigma_u, 0.9 * sigma_y)
        thickness = self.b * kC * np.srt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def aluminum_thickness(self, pressure, k2, kC):
        sigma_u = self.craft.get_sigma_u()
        sigma_y = self.craft.get_sigma_y()
        sigma_d = min(0.6 * sigma_u, 0.9 * sigma_y)
        thickness = self.b * kC * np.srt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def single_skin_plating(self, pressure, k2, kC):
        sigma_d = 0.5 * self.craft.get_sigma_uf()
        thickness = self.b * kC * np.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def wood_plating(self, pressure, k2):
        sigma_d = 0.5 * self.craft.get_sigma_uf()
        thickness = self.b * np.sqrt((pressure * k2)/(1000 * sigma_d))
        return thickness
    
    def fiber_core_plating(self, pressure):
        pass
    
    def wash_plates_plating(self):
        return self.craft.superstructure_deckhouses_pressure()[1]
    
    def watertight_bulkheads_plating(self):
        return self.craft.watertight_bulkheads_pressure()


def main():
    print("ESCANTILLONADO ISO 12215-5 - ISO 12215-5 SCANTLINGS\n")
    designer = input("Diseñador: ")
    boat = input("Embarcación: ")
    company = input("Empresa: ")
    management = input("Gerencia: ")
    division = input("División: ")
    values = {}
    
    print("\nSeleccione la categoría de diseño de su embarcación")
    categories = ('Oceano', 'Offshore', 'Costera', 'Aguas calmadas')
    design_cat = display_menu(categories)
    
    print("\nSeleccione el material de su embarcación")
    available_materials = ('Acero', 'Aluminio', 'Fibra laminada', 'Madera laminada o contrachapada', 'Fibra con nucleo (Sandwich)')
    material = display_menu(available_materials)
    
    # Definir las zonas y sus atributos dependientes
    zones_data = {
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
        'Cubiertas de Operación o Almacenamiento de Vehículos': ['b', 'l', 'c']
    }
    
    craft = Craft(designer, boat, company, management, division, design_cat, material, zone_name=None, zone=None)
    pressure = Pressures(craft, {})
    plating = Plating(craft, {})
    #scantling = Scantlings(craft, material, pressure=pressure, plating=plating)
    
    while True:
        zone_name, zone = get_selected_zone(material, zones_data)
        craft.zone = zone_name, zone
        if zone is None:
            print("\nPrograma finalizado.")
            break
        try:
            required_attributes = zones_data[zone_name]
            zone_attributes = {}
            for attribute in required_attributes:
                zone_attributes[attribute] = getattr(craft, f"get_{attribute}", None)
            pressure.zone_attributes, plating.zone_attributes = zone_attributes
            """Sin embargo, ambos atributos (pressure.zone_attributes y plating.zone_attributes) 
            compartirán la misma referencia en memoria. Si luego modificas pressure.zone_attributes, 
            también se reflejará en plating.zone_attributes."""
            zone_pressure = pressure.calculate_pressure(zone)
            thickness = plating.calculate_plating(zone, zone_pressure)
            values[zone_name] = thickness
            print(f"\nEl espesor mínimo requerido en la zona '{zone_name}' es de: {thickness:.3f} mm")
        except ValueError as e:
            print(e)

def display_menu(items) -> int:
    """Muestra un menú basado en una lista de items y retorna la opción escogida."""
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")
    while True:
        try:
            choice = int(input("Ingrese el número correspondiente -> "))
            if 0 <= choice <= len(items):  # Rango válido
                return choice
            else:
                print("Selección no válida, intente de nuevo.")
        except ValueError:
            print("Entrada no válida, por favor ingrese un número.")
            
def get_selected_zone(material, zones_data) -> tuple:
    """
    Gestiona las zonas según el material seleccionado, muestra al usuario un menú con las zonas
    disponibles y devuelve tanto el nombre de la zona seleccionada como el indice correspondiente.
    """

    # Determinar las zonas disponibles según el material
    available_zones = list(range(1, 12)) if material not in [1, 2] else list(range(1, 14))

    # Crear la lista de nombres de zonas disponibles
    filtered_zone_names = [list(zones_data.keys())[i - 1] for i in available_zones]

    # Mostrar el menú y permitir la selección del usuario
    print("\nSeleccione la zona que desea escantillonar:\
          \n(Ingrese 0 para finalizar el programa)")
    selected_zone_index = display_menu(filtered_zone_names)  # Obtener selección del usuario

    # Verificar si el usuario desea salir
    if selected_zone_index == 0:
        return None, None

    # Mapear el índice seleccionado al nombre de la zona
    zone_name = filtered_zone_names[selected_zone_index - 1]

    # Retornar el nombre de la zona y el número correspondiente
    return zone_name, selected_zone_index

if __name__ == "__main__":
    main()
