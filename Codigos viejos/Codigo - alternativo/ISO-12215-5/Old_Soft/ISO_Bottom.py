from ISO_Craft import Craft
from validations import val_data
from math import sqrt, pow

class Bottom:
    def _init_(self, craft: Craft) -> None:
        self.craft = craft
        #   Atributos internos para almacenar valores
        self.b, self.l, self.s, self.lu, self.c, self.cu = self.specific_attributes()
        self.xp, self.xs = self.determine_x()
        self.kLp, self.kLs = self.calculate_kL()
        self.kRp_displacement, self.kRs_displacement, self.kRp_planning, self.kRs_planning = self.calculate_kR()
        self.ADp, self.ADs = self.calculate_AD()
        self.kARp_displacement, self.kARs_displacement, self.kARp_planning, self.kARs_planning = self.calculate_kAR()
        #   Bottom Factors & Pressures
        self.PBM_MIN = 0.45 * pow(self.craft.mLDC, 0.33) + (0.9 * self.craft.LWL * self.craft.kDC)
        self.PBMDp, self.PBMDs = self._calculate_PBMD()
        self.PBMPp, self.PBMPs = self._calculate_PBMP()
        self.bottom_pressure_p = max(self.PBMDp, self.PBMPp)
        self.bottom_pressure_s = max(self.PBMDs, self.PBMPs)
        #   Bottom Plating
        self.A, self.k1, self.k2, self.k3, self.k4, self.k5, self.k6, self.k7, self.k8 = self.calculate_plating_factors()
        self.kC = self.calculate_kC()
        self.kSHC = self.calculate_kSHC()
        self.t_min, self.w_min, self.wos, self.wis = self.min_hull_thickness()
        self.t, self.SM_0, self.SM_1, self.I, self.EI = self.bottom_plating()
        #   Bottom Stiffeners
        self.kCS = self.calculate_kCS()
        self.AW = self.calculate_AW()
        self.SM = self.calculate_SM()
        self.second_I = self.calculate_second_I()

    def specific_attributes(self) -> tuple:
        b = val_data("\nDigite el lado más corto del panel 'b', entre los 2 rigidizadores más proximos (mm): ") # For a sandwich the b dimension corresponds to the length of a stiffener.
        l = val_data("Digite el lado más largo del panel 'l', entre los 2 rigidizadores más proximos (mm): ", True, True, -1, 0, 330 * self.craft.LH)
        s = val_data("Ingrese la separación entre longitudinales 's' (mm): ", True, True, b)
        lu = val_data("Ingrese la longitud no soportada de los rigidizadores 'lu' (mm): ", True, True, l)
        c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
        cu = val_data("Ingrese la corona o curvatura del rigidizador 'cu' (mm): ", True, True, 0)
        return b, l, s, lu, c, cu

    def determine_x(self) -> tuple:
        print("\nSi desea calcular el enchapado o los refuerzos en algun punto especifico digite los siguientes datos, caso contrario presione Enter")
        xp = val_data("Ingrese la distancia con respecto a popa del centro del panel analizado 'x_p' (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        xs = val_data("Ingrese la distancia con respecto a popa del centro del refuerzo analizado 'x_s' (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        return xp, xs

    def calculate_kL(self) -> tuple:
        xLWLp = self.xp/self.craft.LWL
        xLWLs = self.xs/self.craft.LWL
        if xLWLp > 0.6:
            kLp = 1
        else:
            kLp = (((1-0.167 * self.craft.nCG)/(0.6))*(xLWLp)) + 0.167 * self.craft.nCG
        if xLWLs > 0.6:
            kLs = 1
        else:
            kLs = (((1-0.167 * self.craft.nCG)/(0.6))*(xLWLs)) + 0.167 * self.craft.nCG
        return kLp, kLs
    
    def calculate_kR(self) -> tuple:
        kRp_planning = kRs_planning = 1
        kRp_displacement = 1.5 - 3e-4 * self.b
        kRs_displacement = 1-2e-4 * self.lu
        return kRp_displacement, kRs_displacement, kRp_planning, kRs_planning

    def calculate_AD(self) -> tuple:
        ADp = min((self.l * self.b) * 1e-6, 2.5 * pow(self.b, 2) * 1e-6)
        ADs = max((self.lu * self.s) * 1e-6, 0.33 * pow(self.lu, 2) * 1e-6)
        return ADp, ADs

    def calculate_kAR(self) -> tuple:
        _kARp_planning = (self.kRp_planning * 0.1 * pow(self.craft.mLDC, 0.15)) / pow(self.ADp, 0.3)
        _kARs_planning = (self.kRs_planning * 0.1 * pow(self.craft.mLDC, 0.15)) / pow(self.ADs, 0.3)
        _kARp_displacement = (self.kRp_displacement * 0.1 * pow(self.craft.mLDC, 0.15)) / pow(self.ADp, 0.3)
        _kARs_displacement = (self.kRs_displacement * 0.1 * pow(self.craft.mLDC, 0.15)) / pow(self.ADs, 0.3)
        
        kARp_planning = max(min(_kARp_planning, 1), 0.25)
        kARs_planning = max(min( _kARs_planning, 1), 0.25)
        kARp_displacement = max(min(_kARp_displacement, 1), 0.25)
        kARs_displacement = max(min(_kARs_displacement, 1), 0.25)
        
        return kARp_displacement, kARs_displacement, kARp_planning, kARs_planning

    def _calculate_PBMD(self) -> tuple:
        PBMD_BASE = 2.4 * pow(self.craft.mLDC, 0.33) + 20
        PBMDp = max(PBMD_BASE * self.kARp_displacement * self.craft.kDC * self.kLp, self.PBM_MIN)
        PBMDs = max(PBMD_BASE * self.kARs_displacement * self.craft.kDC * self.kLs, self.PBM_MIN)
        return PBMDp, PBMDs

    def _calculate_PBMP(self) -> tuple:
        PBMP_BASE = ((0.1 * self.craft.mLDC)/(self.craft.LWL * self.craft.BC)) * (1 + pow(self.craft.kDC, 0.5) * self.craft.nCG)
        PBMPp = max(PBMP_BASE * self.kARp_planning * self.kLp, self.PBM_MIN)
        PBMPs = max(PBMP_BASE * self.kARs_planning * self.kLs, self.PBM_MIN)
        return PBMPp, PBMPs

    """
    For bottom, deck and superstructures, the design pressure is constant
    and shall be applied as defined in Clause 8.
    """

    def calculate_plating_factors(self) -> tuple:
        A = k1 = k2 = k3 = k4 = k5 = k6 = k7 = k8 = None
        A = 1 if self.craft.material in ['Acero', 'Aluminio'] else 1.5
        k1 = 0.017
        ar = self.l / self.b
        k2 = min(max((0.271 * pow(ar, 2) + 0.910 * ar - 0.554) / (pow(ar, 2) - 0.313 * ar + 1.351), 0.308), 0.5)
        k3 = min(max((0.027 * pow(ar, 2) - 0.029 * ar + 0.011) / (pow(ar, 2) - 1.463 * ar + 1.108), 0.014), 0.028)
        k4 = 0.9
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

    def min_hull_thickness(self) -> tuple:
        t_min, w_min, wos, wis = None, None, None, None
        if self.craft.material == 'Acero':
            t_min =  self.k5 * (self.A + self.k7 * self.craft.V + self.k8 * pow(self.craft.mLDC, 0.33))
        elif self.craft.material == 'Aluminio':
            t_min =  self.k5 * (self.A + self.k7 * self.craft.V + self.k8 * pow(self.craft.mLDC, 0.33))
        elif self.craft.material == 'FRP-Single Skin':
            w_min = 0.43 * self.k5 * (self.A + self.k7 * self.craft.V + self.k8 * pow(self.craft.mLDC, 0.33))
        elif self.craft.material == 'FRP-Sandwich':
            wos = self.craft.kDC * self.k4 * self.k5 * self.k6 * (0.1 * self.craft.LWL + 0.15)
            wis = 0.7 * wos
        return t_min, w_min, wos, wis

    def bottom_plating(self) -> tuple:
        t = SM_0 = SM_1 = I = EI = None
        if self.craft.material in ['Acero', 'Aluminio']:
            t = max(self.t_min, self.b * self.kC * sqrt((self.bottom_pressure_p * self.k2)/(1000 * self.craft.sigma_dp)))
        elif self.craft.material == 'FRP-Single Skin':
            t = self.b * self.kC * sqrt((self.bottom_pressure_p * self.k2)/(1000 * self.craft.sigma_dp))
        elif self.craft.material == 'FRP-Sandwich':
            b = min(self.b, 330 * self.craft.LWL)
            #   Módulo de sección mínimo requerido de la piel o/i del sándwich de 1 cm de ancho
            SM_0 = (pow(b, 2) * pow(self.kC, 2) * self.bottom_pressure_p * self.k2)/(6e5 * self.craft.sigma_dtp)
            SM_1 = (pow(b, 2) * pow(self.kC, 2) * self.bottom_pressure_p * self.k2)/(6e5 * self.craft.sigma_dcp)
            #   Segundo momento de inercia mínimo requerido para una lamina de sandwich de 1 cm de ancho
            I = (pow(b, 3) * pow(self.kC, 3) * self.bottom_pressure_p * self.k3)/(12e6 * self.k1 * self.craft.Eio)
            EI = (pow(b, 3) * pow(self.kC, 3) * self.bottom_pressure_p * self.k3)/(12e3 * self.k1)
            t = sqrt(self.kC)*((self.kSHC * self.bottom_pressure_p * self.b)/(1000 * self.craft.tau_dp))
        else:
            raise ValueError(f"Material '{self.craft.material}' no reconocido")
        return t, SM_0, SM_1, I, EI

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

    def calculate_AW(self) -> float:
        AW = ((self.craft.kSA * self.bottom_pressure_s * self.s * self.lu)/(self.craft.tau_ds)) * 1e-6
        return AW

    def calculate_SM(self) -> float:
        SM = ((83.33 * self.kCS * self.bottom_pressure_s * self.s * pow(self.lu, 2)) / (self.craft.sigma_ds)) * 1e-9
        return SM

    def calculate_second_I(self) -> float:
        if self.craft.material in ['FRP-Single Skin', 'FRP-Sandwich']:
            I = ((26 * pow(self.kCS, 1.5) * self.bottom_pressure_s * self.s * pow(self.lu, 3))/(0.05 * self.craft.Eio)) * 1e-11
            return I
        return None
