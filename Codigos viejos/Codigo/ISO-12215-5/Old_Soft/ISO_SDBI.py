from ISO_Craft import Craft
from validations import val_data
from math import sqrt, pow, isclose

class SDBI:
    def __init__(self, craft: Craft) -> None:
        self.craft = craft
        #   Atributos internos para almacenar valores
        self.b, self.l, self.s, self.lu, self.c, self.cu = self.specific_attributes()
        self.xp, self.xs = self.determine_x()
        self.kLp, self.kLs = self.calculate_kL()
        self.kRp, self.kRs = self.calculate_kR()
        self.ADp, self.ADs = self.calculate_AD()
        self.kARp, self.kARs = self.calculate_kAR()
        #   SDBI Pressures
        self.PSDS_pressure_p, self.PSDS_pressure_s, self.PWB_p, self.PWB_s, self.PTB_p, self.PTB_s  = self.calculate_PSDS()
        #   Bottom Plating
        self.A, self.k1, self.k2, self.k3, self.k4, self.k5, self.k6, self.k7, self.k8 = self.calculate_plating_factors()
        self.kC = self.calculate_kC()
        self.kSHC = self.calculate_kSHC()
        self.t_min, self.w_min, self.wos, self.wis = self.min_sdbi_thickness()
        self.t, self.SM_0, self.SM_1, self.I, self.EI = self.sdbi_plating()
        #   Bottom Stiffeners
        self.kCS = self.calculate_kCS()
        self.AW_values = self.calculate_AW()
        self.SM_values = self.calculate_SM()
        
        self.second_I = self.calculate_second_I()
        
        
        
        #   SDBI Plating
        self.t_values = self._metal_plating()

        self.SDBI_thickness = [max(self.t_min, i) for i in self.t_values]
        

    def specific_attributes(self) -> tuple:
        b = val_data("\nDigite el lado más corto del panel 'b', entre los 2 rigidizadores más proximos (mm): ") # For a sandwich the b dimension corresponds to the length of a stiffener.
        l = val_data("Digite el lado más largo del panel 'l', entre los 2 rigidizadores más proximos (mm): ", True, True, -1, 0, 330 * self.craft.LH)
        s = val_data("Ingrese la separación entre cuadernas 's' (mm): ")
        lu = val_data("Ingrese la longitud no soportada de los rigidizadores 'lu' (mm): ", True, True, -1, 0, 330 * self.craft.LH)
        self.hp = val_data("Ingrese la altura de la columna de agua para el enchapado del mamparo o tanque integral (metros): ")
        self.hs = val_data("Ingrese la altura de la columna de agua para el refuerzo del mamparo o tanque integral (metros): ")
        c = val_data("Ingrese la corona del panel 'c' (mm): ")
        cu = val_data("Ingrese la corona del rigidizador curvo 'cu' (mm): ")
        return b, l, s, lu, c, cu

    def determine_x(self) -> tuple:
        print("\nSi desea calcular el enchapado o los refuerzos en algun punto especifico digite los siguientes datos, caso contrario presione Enter")
        xp = val_data("Ingrese la distancia con respecto a popa del centro del panel analizado 'x_p' (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        xs = val_data("Ingrese la distancia con respecto a popa del centro del refuerzo analizado 'x_s' (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        return xp, xs

    def calculate_kL(self) -> tuple:
        xLWLp = self.xp/self.craft.LWL
        if xLWLp > 0.6:
            kLp = 1
        else:
            kLp = (((1-0.167 * self.craft.nCG)/(0.6))*(xLWLp)) + 0.167 * self.craft.nCG
        xLWLs = self.xs/self.craft.LWL
        if xLWLs > 0.6:
            kLs = 1
        else:
            kLs = (((1-0.167 * self.craft.nCG)/(0.6))*(xLWLs)) + 0.167 * self.craft.nCG
        return kLp, kLs
    
    def calculate_kR(self) -> tuple:
        if self.craft.type == 'Displacement':
            kRp = 1.5 - 3e10-4 * self.b
            kRs = 1-2e-4 * self.lu       
        else:   #'Planning':
            kRp = kRs = 1
        return kRp, kRs

    def calculate_AD(self) -> tuple:
        ADp = min((self.l * self.b) * 1e-6, 2.5 * pow(self.b, 2) * 1e-6)
        ADs = max((self.lu * self.s) * 1e-6, 0.33 * pow(self.lu, 2) * 1e-6)
        return ADp, ADs

    def calculate_kAR(self) -> tuple:
        _kARp = (self.kRp * 0.1 * pow(self.craft.mLDC, 0.15)) / pow(self.ADp, 0.3)
        _kARs = (self.kRs * 0.1 * pow(self.craft.mLDC, 0.15)) / pow(self.ADs, 0.3)
        kARp = max(min(_kARp, 1), 0.25)
        kARs = max(min(_kARs, 1), 0.25)
        return kARp, kARs

    def calculate_PSDS(self) -> tuple:
        PDM_MIN = 5
        PDM_BASE = 0.35 * self.craft.LWL + 14.6
        PSUPM_kSUP_p_values= {
            'Front': max(PDM_BASE * self.craft.kDC * self.kARp * 1, PDM_MIN),
            'Side (Walking Area)': max(PDM_BASE * self.craft.kDC * self.kARp * 0.67, PDM_MIN),
            'Side (Non Walking Area)': PDM_BASE * self.craft.kDC * self.kARp * 0.5,
            'Aft end': max(PDM_BASE * self.craft.kDC * self.kARp * 0.5, PDM_MIN),
            'Top <= 800 mm above deck': max(PDM_BASE * self.craft.kDC * self.kARp * 0.5, PDM_MIN), #Walking area
            'Top > 800mm above deck': max(PDM_BASE * self.craft.kDC * self.kARp * 0.35, PDM_MIN), #Walking area
            'Upper_Tiers': max(PDM_BASE * self.craft.kDC * self.kARp * 0.35, PDM_MIN)
        }
        PSUPM_kSUP_s_values= {
            'Front': max(PDM_BASE * self.craft.kDC * self.kARs * 1, PDM_MIN),
            'Side (Walking Area)': max(PDM_BASE * self.craft.kDC * self.kARs* 0.67, PDM_MIN),
            'Side (Non Walking Area)': PDM_BASE * self.craft.kDC * self.kARs * 0.5,
            'Aft end': max(PDM_BASE * self.craft.kDC * self.kARs * 0.5, PDM_MIN),
            'Top <= 800 mm above deck': max(PDM_BASE * self.craft.kDC * self.kARs * 0.5, PDM_MIN), #Walking area
            'Top > 800mm above deck': max(PDM_BASE * self.craft.kDC * self.kARs * 0.35, PDM_MIN), #Walking area
            'Upper_Tiers': max(PDM_BASE * self.craft.kDC * self.kARs * 0.35, PDM_MIN)
        }
        p_values_tuple = tuple(PSUPM_kSUP_p_values.values())
        s_values_tuple = tuple(PSUPM_kSUP_s_values.values())
        PWB_p = 7 * self.hp
        PWB_s = 7 * self.hs
        PTB_p = 10 * self.hp
        PTB_s = 10 * self.hs
        return p_values_tuple, s_values_tuple, PWB_p, PWB_s, PTB_p, PTB_s

    """
        8.3.3 Wash plates
        Tanks shall be subdivided as necessary by internal baffles or wash plates. Baffles or wash plates that support
        hull framing shall have scantlings equivalent to stiffeners located in the same position.
        Wash plates and wash bulkheads shall, in general, have an area of perforation not < 50 % of the total area of
        the bulkhead. The perforations shall be so arranged that the efficiency of the bulkheads as a support is not
        impaired.
        The general stiffener requirement for both minimum section modulus and second moment of area may be
        50 % of that required for stiffener members of integral tanks.

        8.3.4 Collision bulkheads
        The scantlings of collision bulkheads, where fitted, shall not be less than required for integral tank bulkheads.

        8.3.5 Non-watertight or partial bulkheads
        Where a bulkhead is structural but non-watertight, the scantlings shall be as required in 11.8.
        Bulkheads and partial bulkheads that are non-structural are outside the scope of this part of ISO 12215.

        8.3.6 Transmission of pillar loads
        Bulkheads that are required to act as pillars in the way of under-deck girders subjected to concentrated loads
        and other structures that carry heavy loads shall be dimensioned according to these loads. See ISO 12215-9
        for mast step analysis for sailing craft.
    """

    def calculate_plating_factors(self) -> tuple:
        A = k1 = k2 = k3 = k4 = k5 = k6 = k7 = k8 = None
        A = 1 if self.craft.material in ['Acero', 'Aluminio'] else 1.5
        k1 = 0.017
        ar = self.l / self.b
        lib = (2.0,1.9,1.8,1.7,1.6,1.5,1.4,1.3,1.2,1.1,1.0)
        k2_values = (0.497,0.493,0.487,0.479,0.468,0.454,0.436,0.412,0.383,0.349,0.308)
        k3_values = (0.028,0.027,0.027,0.026,0.025,0.024,0.023,0.021,0.019,0.016,0.014)
        # Comparar con tolerancia
        if any(isclose(ar, val, rel_tol=1e-9) for val in lib):
            k2 = k2_values[lib.index(ar)]
            k3 = k3_values[lib.index(ar)]
        elif ar > 2:
            k2 = 0.5
            k3 = 0.5
        else:
            k2 = min(max((0.271 * pow(ar, 2) + 0.910 * ar - 0.554) / (pow(ar, 2) - 0.313 * ar + 1.351), 0.308), 0.5)
            k3 = min(max((0.027 * pow(ar, 2) - 0.029 * ar + 0.011) / (pow(ar, 2) - 1.463 * ar + 1.108), 0.014), 0.028)
        k4 = 1
        if self.craft.material == 'Acero':
            k5 = sqrt(240/self.craft.sigma_y)
            k7 = 0.015
            k8 = 0.08    
        elif self.craft.material == 'Aluminio':
            k5 = sqrt(125/self.craft.sigma_y)
            k7 = 0.02
            k8 = 0.1
        elif self.craft.material in ['FRP-Single Skin', 'FRP-Sandwich']: 
            if self.craft.skin == 'Fibra de vidrio E con filamentos cortados':
                k5 = 1.0
            elif self.craft.skin == 'Fibra de vidrio tejida':
                k5 = 0.9
            elif self.craft.skin == 'Fibra tejida de carbono, aramida(kevlar) o híbrida':
                k5 = 0.7
            k6 = 1 
            k7 = 0.03
            k8 = 0.15
        return A, k1, k2, k3, k4, k5, k6, k7, k8

    def calculate_kC(self) -> float:
        #    Curvature correction factor kC for curved plates
        cb = self.c / self.b
        if cb < 0.03: 
            return 1
        elif 0.03 < cb < 0.18:
            return (1.1 - (3.33 * self.c)/self.b)
        else:
            return 0.5

    def calculate_kSHC(self) -> float:
        ar = self.l / self.b
        lib = (4.0, 3.0, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0)
        kSHC_values = (0.500, 0.493, 0.463, 0.459, 0.453, 0.445, 0.435, 0.424, 0.410, 0.395, 0.378, 0.360, 0.339)
        if ar <= 2:
            return 0.035 + 0.394 * ar - 0.09 * pow(ar, 2)
        elif ar > 4:
            return 0.500
        else:
            # Interpolación
            for i in range(len(lib) - 1):
                if lib[i] >= ar > lib[i + 1]:
                    x1, y1 = lib[i], kSHC_values[i]
                    x2, y2 = lib[i + 1], kSHC_values[i + 1]
                    return y1 + (y2 - y1) / (x2 - x1) * (ar - x1)
            # En caso de que, por algún motivo, no se haya devuelto un valor en el loop anterior
            return 0.500

    def min_sdbi_thickness(self) -> float:
        if self.craft.material == 'Acero':
            t_min =  1.5 + 0.07 * self.craft.LWL
        elif self.craft.material == 'Aluminio':
            t_min = 1.35 + 0.06 * self.craft.LWL
        elif self.craft.material in ['FRP-Single Skin', 'FRP-Sandwich']:
            t_min = self.k5 * (1.45 + 0.14 * self.craft.LWL)
        elif self.craft.material in ["Wood", "plywood"]:
            t_min = 3.8 + 0.17 * self.craft.LWL
        else:
            raise ValueError(f"Material {self.craft.material} no reconocido")
        return t_min

    def deck_plating(self) -> tuple: # quede por aqui
        t = SM_0 = SM_1 = I = EI = None
        if self.craft.material in ['Acero', 'Aluminio']:
            t = max(self.t_min, self.b * self.kC * sqrt((self.deck_pressure_p * self.k2)/(1000 * self.craft.sigma_dp)))
        elif self.craft.material == 'FRP-Single Skin':
            t = self.b * self.kC * sqrt((self.deck_pressure_p * self.k2)/(1000 * self.craft.sigma_dp))
        elif self.craft.material == 'FRP-Sandwich':
            b = min(self.b, 330 * self.craft.LWL)
            #   Módulo de sección mínimo requerido de la piel o/i del sándwich de 1 cm de ancho
            SM_0 = (pow(b, 2) * pow(self.kC, 2) * self.deck_pressure_p* self.k2)/(6e5 * self.craft.sigma_dtp)
            SM_1 = (pow(b, 2) * pow(self.kC, 2) * self.deck_pressure_p * self.k2)/(6e5 * self.craft.sigma_dcp)
            #   Segundo momento de inercia mínimo requerido para una lamina de sandwich de 1 cm de ancho
            I = (pow(b, 3) * pow(self.kC, 3) * self.deck_pressure_p * self.k3)/(12e6 * self.k1 * self.craft.Eio)
            EI = (pow(b, 3) * pow(self.kC, 3) * self.deck_pressure_p * self.k3)/(12e3 * self.k1)
            t = sqrt(self.kC)*((self.kSHC * self.deck_pressure_p* self.b)/(1000 * self.craft.tau_dp))
        else:
            raise ValueError(f"Material '{self.craft.material}' no reconocido")
        return t, SM_0, SM_1, I, EI

    def sdbi_plating(self) -> list:
        pressure = self.PSDS_pressure_p + (self.PWB_p, self.PTB_p)
        t_values = []
        for i in range(len(pressure)):
            t_values.append(self.b * self.kC * sqrt((pressure[i] * self.k2)/(1000 * self.craft.sigma_dp)))
        return t_values

    """
    La rigidez relativa de los elementos de refuerzo primario y secundario 
    deberá ser tal que las cargas se transfieran eficazmente del secundario 
    al primario y, luego al enchapado y a los mamparos.
    """

    def calculate_kCS(self) -> float:
        culu = self.cu / self.lu
        if culu <= 0.03:
            kCS = 1
        elif 0.03 < culu <= 0.18:
            kCS = 1.1 - 3.33 * culu
        else:
            kCS = 0.5
        return kCS

    def calculate_AW(self) -> list:
        pressure = self.PSDS_pressure_s + (self.PWB_s, self.PTB_s)
        AW_values = []
        for i in range(len(pressure)):
            AW_value = ((self.craft.kSA * pressure[i] * self.s * self.lu)/(self.craft.tau_ds)) * 1e-6
            AW_values.append(AW_value)
        return AW_values

    def calculate_SM(self) -> list:
        pressure = self.PSDS_pressure_s + (self.PWB_s, self.PTB_s)
        SM_values = []
        for i in range(len(pressure)):
            SM_value = ((83.33 * self.kCS * pressure[i] * self.s * pow(self.lu, 2)) / (self.craft.sigma_ds)) * 1e-9
            SM_values.append(SM_value)
        return SM_values

    def calculate_second_I(self) -> float: # arreglar esto
        if self.craft.material in ['FRP-Single Skin', 'FRP-Sandwich']:
            I = ((26 * pow(self.kCS, 1.5) * self.SDBI_pressure_s * self.s * pow(self.lu, 3))/(0.05 * self.craft.Eio)) * 1e-11
            return I
        return None
