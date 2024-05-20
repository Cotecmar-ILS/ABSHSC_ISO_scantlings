# Bottom Shell
# Side Shell
# Decks
# Superstructure and Deckhouses – Front, Sides, Ends, and Tops
# Tank Bulkheads
# Watertight Bulkheads


from new_craft import Craft
import numpy as np


class pressures:


    def __init__(self, craft: Craft):
        self.craft = craft
        #   Atributos internos para almacenar valores
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        # self.tau = val_data("\nIngrese el ajuste de navegación o trim (tao), en grados: ", True, True, 0, 3)
        # self.lp = val_data("\nDigite el borde más largo del panel de la placa, en cm: ")
        # self.sp = val_data("Digite el borde más corto del panel de la placa, en cm: ")
        # self.l = val_data("\nIngrese la longitud sin apoyo del refuerzo en cm: ")
        # self.s = val_data("Ingrese la separación de los longitudinales o rigidizadores del fondo, en cm: ")
        # self.h13 = self.calculate_h13()
        self.ncg = self.calculate_ncg()
        # self.FDp, self.FDs = self.calculate_FD()
        # self.FV = self.calculate_FV()
        
    
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
        ncg_limit = 1.39 + kn * (self.craft.V / np.sqrt(self.craft.L))
        _ncg = self.N2 * (((12 * self.h13) / self.craft.BW) + 1) * self.tau * (50 - self.craft.Bcg) * ((pow(self.craft.V, 2) * pow(self.craft.BW, 2)) / self.craft.W)
        ncg = min(ncg_limit, _ncg)
        if self.craft.V > (18 * np.sqrt(self.craft.L)):
            opcion = val_data("\nIngrese 1 si su embarcación es regular o 2 si es de búsqueda y rescate\n")
            if opcion == 1: #embarcación regular
                ncg = 6
            else:   #embarcación de búsqueda y rescate
                ncg = 7
        if self.craft.L < 24 and ncg < 1:
            ncg = 1
        return ncg
     
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
        Lx = val_data("Ingrese la distancia a popa donde se esta realizando los calculos (metros): ", True, True, 0)
        Fx = Lx / self.craft.L
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
    
    
    
    def bottom_pressure(self):
        slamming_pressure_less61 = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + self.ncg) * self.FDp * self.FV)
        hidrostatic_pressure = self.N3 * (0.64 * self.h13 + self.craft.d)
        return max (slamming_pressure_less61, hidrostatic_pressure)

    def side_transom_pressure(self):
        slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + self.nxx) * ((70 - self.Bsx) / (70 - self.Bcg)) * self.FD
        hidrostatic_pressure = self.N3 * (self.Hs - y)
        # where L is generally not to be taken less than 30 m page 71
        fore_end = 0.28 * Fa * Cp * N3 * (0.22 + 0.15 * np.tan(alfa)) * ((0.4 * self.craft.V * np.cos(beta) + 0.6 * self.craft.L ** 0.5) ** 2)
        return max(slamming_pressure, hidrostatic_pressure) if self.craft.L < 30 else max(slamming_pressure, hidrostatic_pressure), fore_end
    
    
    #revisar de aqui para abajo
    def wet_deck_pressure(self):
        deck_pressure = 30 * self.N1 * self.FD * self.F1 * self.craft.V * self.v1 * (1 - 0.85 * self.ha / self.h13)
        return deck_pressure
    
    def decks_pressures(self):
        pass
    
    def superstructures_pressures(self):
        pass
    
    def bulkheads_pressures(self):
        pass
    
    