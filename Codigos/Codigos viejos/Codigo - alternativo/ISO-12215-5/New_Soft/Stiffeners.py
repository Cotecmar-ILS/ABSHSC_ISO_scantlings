from General import Craft
from Pressures import Pressure
from ABS_HSC.validations import val_data

#Plating shall be supported by an arrangement of stiffening members
class Stiffener():
    def __init__(self, craft: Craft, pressure: Pressure):
        self.craft = craft
        self.pressure = pressure
        self.kSA = 5.0
        
    def curvature_factor_for_stiffeners_kCS(self, cu, lu):
        culu = cu / lu
        if culu <= 0.03:
            kCS = 1.0
        elif culu <= 0.18 and culu > 0.03: #Modificado
            kCS = 1.1 - 3.33 * (cu / lu)
        else:  # cb > 0.18
            kCS = 0.5
        # Aplica las restricciones de que kCS no debe ser menor a 0.5 ni mayor a 1.0
        kCS = max(min(kCS, 1.0), 0.5)
        return kCS
            
    #Stiffeners equiations based on different materials
    def web_area_AW(self, pressure, s, lu, tau):
        if self.craft.material == 'Fibra laminada':
            tau_d = 0.5 * tau
        elif self.craft.material == self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            tau_d = 0.5 * tau
        elif self.craft.material == 'Fibra con nucleo (Sandwich)':
            tau_d = 0.5 * tau
        elif self.craft.material == 'Madera (laminada y plywood)':
            tau_d = 0.5 * tau
        else:
            tau_d = 0.5 * tau
        AW = ((self.kSA * pressure * s * lu)/(tau_d)) * 1e-6
        return AW
    
    def min_section_modulus_SM(self, pressure, s, lu, cu, sigma):
        kCS = self.curvature_factor_for_stiffeners_kCS(cu, lu)
        if self.craft.material == 'Fibra laminada':
            sigma_d = 0.5 * sigma
        elif self.craft.material == self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            sigma_d = 0.5 * sigma
        elif self.craft.material == 'Fibra con nucleo (Sandwich)':
            sigma_d = 0.5 * sigma
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_d = 0.5 * sigma
        else:
            sigma_d = 0.5 * sigma
        SM = ((83.33 * kCS * pressure * s * (lu**2)) / (sigma_d)) * 1e-9
        return SM
    
    def supplementary_stiffness_requirements_for_FRP(self, pressure, s, lu, cu):
        kCS = self.curvature_factor_for_stiffeners_kCS(cu, lu)
        Etc = val_data(f"Ingrese el promedio del módulo de compresión y de tensión de la {self.craft.material} para el refuerzo: ", True, True, -1, 0.001)
        I = ((26 * (kCS**1.5) * pressure * s * (lu**3))/(0.05 * Etc)) * 1e-11
        return I
    
    #Stiffeners requirements based on different zones
    def stiffeners(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para los refuerzos de: {self.craft.zone}\n")
        s = val_data("Ingrese la separación entre refuerzos 's' (mm): ", True, True)
        lu = val_data("Ingrese la longitud no soportada de los refuerzos 'lu' (mm): ", True, True)
        cu = val_data("Ingrese la corona o curvatura si el refuerzo es curvo 'cu', en caso contrario presione Enter (mm): ", True, True, 0)
        x = val_data("Ingrese la distancia desde la popa hasta la posición longitudinal del centro del panel o centro del refuerzo analizado, caso contrario presione Enter (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        pressure = self.pressure.get_zone_pressure(b=None, l=None, s=s, lu=lu, x=x)
        
        if self.craft.material in ['Fibra laminada', 'Fibra con nucleo (Sandwich)']:
            tau = val_data(f"Ingrese la resistencia última mínima al cortante de la {self.craft.material} para el refuerzo: ", True, True, -1, 0.001)
            sigma_ct = val_data(f"Ingrese esfuerzo último (compresión o tracción) de la {self.craft.material} según el tipo de carga presente en el refuerzo: ", True, True, -1, 0.001)
            AW = self.web_area_AW(pressure, s, lu, tau)
            SM = self.min_section_modulus_SM(pressure, s, lu, cu, sigma_ct)
            I = self.supplementary_stiffness_requirements_for_FRP(pressure, s, lu, cu)
            return AW, SM, I
        elif self.craft.material in ['Acero', 'Aluminio']:
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001)
            AW = self.web_area_AW(pressure, s, lu, sigma_y)
            SM = self.min_section_modulus_SM(pressure, s, lu, cu, sigma_y)
            return AW, SM
        else: #self.craft.material == 'Madera (laminada y plywood)':
            tau = val_data(f"Ingrese la resistencia última mínima al cortante de la {self.craft.material} para el refuerzo: ", True, True, -1, 0.001)
            sigma_uf = val_data(f"Ingrese la esfuerzo último a la flexión de la {self.craft.material} para el refuerzo: ", True, True, -1, 0.001)
            AW = self.web_area_AW(pressure, s, lu, tau)
            SM = self.min_section_modulus_SM(pressure, s, lu, cu, sigma_uf)
            return AW, SM