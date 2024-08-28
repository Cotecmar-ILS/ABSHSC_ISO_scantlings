from General import Craft
from ABS_HSC.validations import val_data

class Pressure():
    def __init__(self, craft: Craft):
        self.craft = craft
        self.PBMD_BASE = 2.4 * (self.craft.mLDC**0.33) + 20
        self.PBMP_BASE = ((0.1 * self.craft.mLDC)/(self.craft.LWL * self.craft.BC))*((1+self.design_category_kDC()**0.5) * self.dynamic_load_nCG())
        self.PBM_MIN = 0.45 * (self.craft.mLDC ** 0.33) + (0.9 * self.craft.LWL * self.design_category_kDC())
        self.PSM_MIN = 0.9 * self.craft.LWL * self.design_category_kDC()
        self.PDM_BASE = 0.35 * self.craft.LWL + 14.6
        self.PDM_MIN = 5
        
    #Función para exportar la presión requerida (NUEVA)
    def get_zone_pressure(self, b, l, s, lu, x):
        if self.craft.zone == 'Fondo':
            return self.bottom_pressure(b, l, s, lu, x)
        elif self.craft.zone == 'Costados y Espejo':
            return self.side_transom_pressure(b, l, s, lu, x)
        elif self.craft.zone == 'Cubierta':
            return self.deck_pressure(b, l, s, lu, x)
        elif self.craft.zone == 'Superestructura':
            return self.superstructures_deckhouses_pressure(b, l, s, lu)
        elif self.craft.zone == 'Mamparos estancos':
            return self.watertight_bulkheads_pressure()
        elif self.craft.zone == 'Mamparos de tanques integrales':
            return self.integral_tank_bulkheads_pressure()
        elif self.craft.zone == 'Placas anti oleaje':
            return self.wash_plates_pressure()
        elif self.craft.zone == 'Mamparos de colisión':
            return self.collision_bulkheads_pressure()
        else:
            raise ValueError(f"Zona '{self.craft.zone}' no reconocida o no implementada.")
    
    #Pressure Adjusting Factors
    def design_category_kDC(self):
        if self.craft.category == 'A':
            kDC = 1
        elif self.craft.category == 'B':
            kDC = 0.8
        elif self.craft.category == 'C':
            kDC = 0.6
        else:
            kDC = 0.4
        return kDC
    
    def dynamic_load_nCG(self):
        """
        Calcula el factor de carga dinámica nCG para embarcaciones de motor en modo de planeo.
        Retorna:
        float: El valor de nCG, limitado a un máximo de 7.
        """
        # Primero calculamos nCG usando la ecuación (1)
        nCG_1 = 0.32 * ((self.craft.LWL / (10 * self.craft.BC)) + 0.084) * (50 - self.craft.B04) * ((self.craft.V**2 * self.craft.BC**2) / self.craft.mLDC)
        # Luego calculamos nCG usando la ecuación (2)
        nCG_2 = (0.5 * self.craft.V) / (self.craft.mLDC**0.17)
        # Si nCG_1 es mayor que 3, usamos el menor entre nCG_1 y nCG_2
        if nCG_1 > 3:
            nCG = min(nCG_1, nCG_2)
        else:
            nCG = nCG_1  # Si nCG_1 es menor o igual a 3, lo usamos directamente
        # Nos aseguramos de que nCG no sea mayor que 7
        nCG = min(nCG, 7)
        # Si nCG es mayor que 7, imprimimos una advertencia
        if nCG > 7:
            print(f"\nCUIDADO: El valor de carga dinámica (nCG)= {nCG} no debe ser mayor a 7, revise sus parametros iniciales")
        return nCG

    def longitudinal_pressure_distribution_kL(self, x):
        """
        Parámetros:
        x (float): Posición a lo largo de la longitud de la línea de flotación (LWL).
        """
        # Calcula x/LWL
        xLWL = x / self.craft.LWL
        # Si x/LWL es mayor que 0.6, kL es 1
        if xLWL > 0.6:
            kL = 1
        else:
            # Limita nCG entre 3 y 6 para calcular kL
            nCG_clamped = min(max(self.dynamic_load_nCG(), 3), 6)
            # Aplica la ecuación para valores de x/LWL <= 0.6
            kL = ((1 - 0.167 * nCG_clamped) * xLWL / 0.6) + (0.167 * nCG_clamped)
        return kL

    def area_pressure_reduction_kAR(self, b, l, s, lu):
        """
        Retorna:
        float: El valor de kAR ajustado al material y limitado a un máximo de 1.
        """
        # Cálculo de AD dependiendo del contexto
        if self.craft.context == 'Plating':
            AD = min((l * b) * 1e-6, 2.5 * (b**2) * 1e-6)
        else:  # 'Stiffeners'
            AD = max((lu * s) * 1e-6, 0.33 * (lu**2) * 1e-6)
        # Cálculo de kR dependiendo del contexto
        kR = 1.5 - 3e-4 * b if self.craft.context == 'Plating' else 1 - 2e-4 * lu
        # Asegurar que kR no sea menor que el valor para el planeo
        kR = max(kR, 1.0)
        # Calculo de kAR
        kAR = (kR * 0.1 * (self.craft.mLDC**0.15)) / (AD**0.3)
        kAR = min(kAR, 1)  # kAR no debe ser mayor que 1
        # Ajustes basados en el material
        min_kAR = 0.4 if self.craft.material == 'Fibra con nucleo (Sandwich)' else 0.25
        kAR = max(min_kAR, kAR)
        return kAR

    def hull_side_pressure_reduction_kZ(self):
        Z = val_data("Ingrese la altura de la cubierta, medida desde la linea de flotación (metros): ", True, True, 1, 0.0001)
        if self.craft.context == 'Plating':
            h = val_data("Ingrese la altura del centro del panel por encima de la linea de flotación (metros): ", True, True, 0, 0, Z)
        else:
            h = val_data("Ingrese la altura del centro del refuerzo por encima de la linea de flotación (metros): ", True, True, 0, 0, Z)
        return (Z-h)/Z
    
    def superstructure_deckhouse_pressure_reduction_kSUP(self):
        # Devuelve un diccionario con todos los valores de kSUP
        kSUP_values = {
            'Front': 1,
            'Side (Walking Area)': 0.67,
            'Side (Non Walking Area)': 0.5,
            'Aft end': 0.5,
            'Top <= 800 mm above deck': 0.5,  # Área de caminata
            'Top > 800mm above deck': 0.35,   # Área de caminata
            'Upper_Tiers': 0                   # Elementos no expuestos al clima
        }
        return kSUP_values
    
    #Design Pressures
    def bottom_pressure(self, b, l, s, lu, x):
        kAR = self.area_pressure_reduction_kAR(b, l, s, lu)
        kL = self.longitudinal_pressure_distribution_kL(x)
        kDC = self.design_category_kDC()

        # Calcula la presión de fondo en modo de desplazamiento
        PBMD = self.PBMD_BASE * kAR * kDC * kL
        # Asegúrate de que la presión no sea inferior al mínimo
        PBMD = max(self.PBM_MIN, PBMD)

        # Calcula la presión de fondo en modo de planeo
        PBMP = self.PBMP_BASE * kAR * kDC * kL
        # Asegúrate de que la presión no sea inferior al mínimo
        PBMP = max(self.PBM_MIN, PBMP)

        # Siempre usa la mayor presión de fondo entre desplazamiento y planeo
        return max(PBMD, PBMP)
    
    def side_transom_pressure(self, b, l, s, lu, x):
        kZ = self.hull_side_pressure_reduction_kZ()
        kAR = self.area_pressure_reduction_kAR(b, l, s, lu)
        kL = self.longitudinal_pressure_distribution_kL(x)
        kDC = self.design_category_kDC()
        # Calculamos las presiones del costado en ambos modos
        PSMD = (self.PDM_BASE + kZ * (self.PBMD_BASE - self.PDM_BASE)) * kAR * kDC * kL
        PSMP = (self.PDM_BASE + kZ * (0.25 * self.PBMP_BASE - self.PDM_BASE)) * kAR * kDC * kL
        # Aplicamos la presión mínima del costado como límite inferior
        PSMD = max(self.PSM_MIN, PSMD)
        PSMP = max(self.PSM_MIN, PSMP)
        side_pressure = max(PSMD, PSMP)
        return side_pressure
    
    def deck_pressure(self, b, l, s, lu, x):
        kAR = self.area_pressure_reduction_kAR(b, l, s, lu)
        kDC = self.design_category_kDC()
        kL = self.longitudinal_pressure_distribution_kL(x)
        # Define PDM_BASE según la normativa
        PDM_BASE = 0.35 * self.craft.LWL + 14.6  # Valor según la ecuación (17)
        # Calcula la presión de cubierta
        PDM = PDM_BASE * kAR * kDC * kL
        # Define PDM_MIN como un valor constante de 5 kN/m²
        PDM_MIN = 5  # Valor según la ecuación (16)
        # Asegúrate de que la presión no sea inferior al mínimo
        PDM = max(PDM_MIN, PDM)
        return PDM

    def superstructures_deckhouses_pressure(self, b, l, s, lu):
        kAR = self.area_pressure_reduction_kAR(b, l, s, lu)
        kDC = self.design_category_kDC()
        kSUP_values = self.superstructure_deckhouse_pressure_reduction_kSUP()
        # Calcula y devuelve un diccionario con las presiones de diseño para cada ubicación posible
        PSUP_M_values = {location: max(self.PDM_BASE * kDC * kAR * kSUP, self.PDM_MIN) for location, kSUP in kSUP_values.items()}
        return PSUP_M_values
    
    @property
    def hB(self):
        return val_data("Ingrese la altura de la columna de agua (en metros): ", True, True, -1, 0.0001) #Modificado
    
    def watertight_bulkheads_pressure(self):
        PWB = 7 * self.hB
        return PWB
    
    def integral_tank_bulkheads_pressure(self):
        PTB = 10 * self.hB
        return PTB
    
    def wash_plates_pressure(self):
        # Calcular el área total del mamparo
        h = val_data("Ingrese la altura del mamparo de tanque integral: ")
        b = val_data("Ingrese la base del mamparo de tanque integral: ")
        area_mamparo_tanque = h * b
        # Calcular el factor de reducción debido a las perforaciones
        # Aviso sobre el área de perforación
        print("Aviso: El área de perforación debe ser mayor al 50'%' del área total del mamparo de tanque integral.")
        area_perforacion = val_data("Ingrese el area de perforacion de la placa anti oleaje: ", True, True, -1, 0.5 * area_mamparo_tanque)
        factor_reduccion = (area_mamparo_tanque - area_perforacion) / area_mamparo_tanque
        # Ajustar la presión hidrostática por el factor de reducción
        PWP = 10 * self.hB * factor_reduccion
        return PWP

    def collision_bulkheads_pressure(self):
        PTB = 10 * self.hB
        return PTB
   
    def structural_bulkheads_pressure(self):
        return print("Verificar norma ISO 12215-5, inciso 8.3.5 & 11.8")
    
    def transmision_pilar_loads_pressure(self):
        return print("Verificar norma ISO 12215-5, inciso 8.3.6")