from ABS_Craft import Craft
from ABS_HSC.validations import val_data
from math import sqrt, pow

class Side:
    def __init__(self, craft: Craft) -> None:
        self.craft = craft
        #   Atributos internos para almacenar valores
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        self.tau = val_data("\nIngrese el ajuste de navegación o trim (tao), en grados: ", True, True, 0, 3)
        self.lp = val_data("\nDigite el borde más largo del panel de la placa, en cm: ")
        self.sp = val_data("Digite el borde más corto del panel de la placa, en cm: ")
        self.l = val_data("\nIngrese la longitud sin apoyo del refuerzo en cm: ")
        self.s = val_data("Ingrese la separación de los longitudinales o rigidizadores del costado, en cm: ")
        self.h13 = self.calculate_h13()
        self.ncg, self.nxx = self.calculate_ncg()
        self.Lx = val_data("Ingrese la distancia desde la Popa hasta donde se están realizando los calculos (metros): ", True, True, -1, 0, self.craft.L)
        self.FDp, self.FDs = self.calculate_FD()
        self.FV = self.calculate_FV()
        #   Plating & Stiffeners Side Pressures
        self.k, self.k1 = self._calculate_k_k1()
        self.sigma_ap = self.dstress_plating("Side")
        self.d_stressp = self.sigma_ap[0] if self._calculate_Pbxx61() > self._calculate_Pd() else self.sigma_ap[1]
        self.bottom_p = self.pressure()
        #   Plating
        self.q = self.calculate_qs_qa()
        self.bottom_t = self.thickness()
        #   Plating
        self.sigma_ai = self.dstress_internals("Side")
        self.d_stressi = (self.sigma_ai[0], self.sigma_ai[1]) if self._calculate_Pbxx61() > self._calculate_Pd() else (self.sigma_ai[2], self.sigma_ai[3])
        self.binternals_SM = self.calculate_internals_SM()
        self.K4 = self.calculate_K4()
        self.E = self.calculate_E()
        self.binternals_I = self.moment_inertia()
        
    def calculate_h13(self) -> float:
        print("\nSeleccione el tipo de embarcacón de diseño:\n1: High-Speed Craft \n2: Coastal Craft \n3: Riverine Craft")
        select = val_data("Ingrese el número correspondiente: ", False, True, 0, 1, 3)
        if select == 1:
           return max(4, (self.craft.L / 12))
        elif select == 2:
            return max(2.5, (self.craft.L / 12))
        else:
            return max(0.5, (self.craft.L / 12))
    
    def calculate_ncg(self) -> float:
        kn = 0.256
        ncg_limit = 1.39 + kn * (self.craft.V / sqrt(self.craft.L))
        _ncg = self.N2 * (((12 * self.h13) / self.craft.BW) + 1) * self.tau * (50 - self.craft.Bcg) * ((pow(self.craft.V, 2) * pow(self.craft.BW, 2)) / self.craft.W)
        ncg = min(ncg_limit, _ncg)
        if self.craft.V > (18 * sqrt(self.craft.L)):
            opcion = val_data("\nIngrese 1 si su embarcación es regular o 2 si es de búsqueda y rescate\n")
            if opcion == 1: #embarcación regular
                ncg = 6
            else:   #embarcación de búsqueda y rescate
                ncg = 7
        if self.craft.L < 24 and ncg < 1:
            ncg = 1
        
        Kv = 0.8  # Valor por defecto
        # Puntos conocidos
        x_known = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        y_known = [0.8, 0.8, 0.8, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        # Si Lx está fuera del rango, tomar el valor extremo más cercano
        if self.Lx <= 0.5:
            return 0.8
        if self.Lx >= 1.0:
            return 2.0
        # Interpolación manual
        for i in range(len(x_known) - 1):
            if x_known[i] <= self.Lx <= x_known[i + 1]:
                Kv = y_known[i] + (y_known[i + 1] - y_known[i]) * (self.Lx - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        nxx = ncg * Kv
        
        return ncg, nxx

    def calculate_FD(self):
        ADp = min(self.lp * self.sp, 2.5 * pow(self.s, 2))
        ADs = max(self.l * self.s, 0.33 * pow(self.l, 2))
        # Calculo de AR
        AR = 6.95 * self.craft.W / self.craft.d
        # Valores de AD/AR
        ADRp = ADp / AR
        ADRs = ADs / AR
        # Puntos conocidos y sus valores correspondientes
        x_known = [0.001, 0.005, 0.010, 0.05, 0.100, 0.500, 1]
        y_known = [1, 0.86, 0.76, 0.47, 0.37, 0.235, 0.2]
        
        # Interpolación manual para ADRp
        FDp = 0.2  # Valor por defecto
        for i in range(len(x_known) - 1):
            if x_known[i] <= ADRp <= x_known[i + 1]:
                FDp = y_known[i] + (y_known[i + 1] - y_known[i]) * (ADRp - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        # Asegurar que FDp esté dentro [0.4, 1.0]
        FDp = min(max(FDp, 0.4), 1.0)
        
        # Interpolación manual para ADRs
        FDs = 0.2  # Valor por defecto
        for i in range(len(x_known) - 1):
            if x_known[i] <= ADRs <= x_known[i + 1]:
                FDs = y_known[i] + (y_known[i + 1] - y_known[i]) * (ADRs - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        # Asegurar que FDs esté dentro [0.4, 1.0]
        FDs = min(max(FDs, 0.4), 1.0)
        
        return FDp, FDs
      
    def calculate_FV(self) -> float:
        print("\n*Nota: Pulse Enter si desea tomar el valor mayor de FV")
        Lx1 = self.craft.L - self.Lx
        Fx = Lx1 / self.craft.LW
        # Puntos conocidos y sus valores correspondientes
        x_known = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.445, 0.4, 0.3, 0.2, 0.1, 0]
        y_known = [0.25, 0.39, 0.52, 0.66, 0.8, 0.92, 1, 1, 1, 1, 1, 0.5]
        # Si Fx es exactamente 0 o 1, retornar los valores correspondientes
        if Fx == 0:
            return 1
        if Fx == 1:
            return 0.25
        # Interpolación manual
        FV = 1  # Valor por defecto
        for i in range(len(x_known) - 1):
            if x_known[i] >= Fx >= x_known[i + 1]:
                FV = y_known[i] + (y_known[i + 1] - y_known[i]) * (Fx - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        # Asegurar que FV esté dentro [0.25, 1.0]
        FV = min(max(FV, 0.25), 1.0)      
        return FV
        
    def calculate_Pbxxx(self) -> float:
        Pbxxx_p = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + nxx) * self.FDp * self.FV)
        Pbxxx_s = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + nxx) * self.FDs * self.FV)
        return Pbxxx_p, Pbxxx_s

    def calculate_Pd(self) -> float:
        H = max(0.0172 * self.craft.L + 3.653, self.h13)
        Pd = self.N3 * (0.64 * H + self.craft.d)
        return Pd

    def pressure(self) -> float:
        bottom_p_p = max(self.Pbxxx_p, self.Pd)
        bottom_p_s = max(self.Pbxxx_s, self.Pd)
        return bottom_p_p, bottom_p_s
    
    def _calculate_k_k1(self) -> float:
        ar_known = [2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0]
        k_known = [0.497, 0.493, 0.487, 0.479, 0.468, 0.454, 0.436, 0.412, 0.383, 0.348, 0.308]
        k1_known = [0.028, 0.027, 0.027, 0.026, 0.025, 0.024, 0.024, 0.021, 0.019, 0.017, 0.014]
        ar = self.lp / self.sp
        if ar > 2.0:
            return 0.500, 0.028
        k_value = k_known[ar_known.index(ar)] if ar in ar_known else np.interp(ar, ar_known, k_known)
        k1_value = k1_known[ar_known.index(ar)] if ar in ar_known else np.interp(ar, ar_known, k1_known)
        return k_value, k1_value
    
    def _lateral_loading(self) -> float:
        t1 = self.s * 10 * sqrt((self.bottom_p * self.k)/(1000*self.d_stressp))
        return t1
    
    def _secondary_stiffening(self) -> float:
        if self.material == 'Acero':
            t2 = 0.01*self.s
        elif self.material == 'Aluminio':
            t2 = 0.012*self.s
        return t2
    
    def calculate_qs_qa(self) -> float:
        if self.material == 'Acero':
            if self.resistencia == 'Ordinaria':
                qs = 1.0
            elif self.resistencia == 'Alta':
                qs = max(0.72, 245/self.sigma_y)
            else:
                qs = 1.0 #Verificar que pasa con resistencias bajas de material
            return qs 
        elif self.material == 'Aluminio':
            qa = 115/self.sigma_y
            return qa
    
    def _minimum_thickness(self) -> float:
        if self.material == 'Acero':
            t3 = max(0.44 * sqrt(self.L * self.q) + 2.0, 3.5)
        elif self.material == 'Aluminio':
            t3 = max(0.70 * sqrt(self.L * self.q) + 1.0, 4.0)
        return t3
    
    def thickness(self) -> float:
        bottom_t = max(self._lateral_loading(), self._secondary_stiffening(), self._minimum_thickness())
        return bottom_t
    
    def calculate_internals_SM(self) -> tuple:
        SM_values = []
        for i in range(len(self.d_stressi)):
            SM = (83.3*self.bottom_p*(self.s/100)*pow((self.l/100),2))/(self.d_stressi[i])
            SM_values.append(SM)
        return tuple(SM_values)
    
    def calculate_K4(self) -> float:
        if self.material == 'Acero':
            if self.zone == "Bottom" or self.zone == "Side":
                return 0.0015
            else:
                return 0.0011
        elif self.material == "Aluminio":
            if self.zone == "Bottom" or self.zone == "Side":
                return 0.0021
            else:
                return 0.0018

    def calculate_E(self) -> float:
        if self.material == 'Acero':
            return 2.06e5
        elif self.material == 'Aluminio':
            return 6.9e4

    def moment_inertia(self) -> float:
        I = (260*self.bottom_p*(self.s/100)*pow((self.l/100),3))/ (self.K4*self.E)
        return I
    