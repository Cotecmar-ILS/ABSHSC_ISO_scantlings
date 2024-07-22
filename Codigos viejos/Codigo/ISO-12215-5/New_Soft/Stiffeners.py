from General import Craft
from Pressures import Pressure
from validations import val_data

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

    #Stiffeners equiations based on different materials3
    def web_area_AW(self, pressure, s, lu, tau_d):
        if self.craft.zone == 'Superestructura':
            return {location: ((self.kSA * pres * s * lu) / tau_d) * 1e-6 for location, pres in pressure.items()}
        else:
            return ((self.kSA * pressure * s * lu)/(tau_d)) * 1e-6

    def min_section_modulus_SM(self, pressure, s, lu, cu, sigma_d):
        if self.craft.zone == 'Superestructura':
            resultados_SM = {}
            for location, pres in pressure.items():
                kCS = self.curvature_factor_for_stiffeners_kCS(cu, lu)
                SM = ((83.33 * kCS * pres * s * (lu**2)) / sigma_d) * 1e-9
                resultados_SM[location] = SM
            return resultados_SM
        else:
            kCS = self.curvature_factor_for_stiffeners_kCS(cu, lu)
            SM = ((83.33 * kCS * pressure * s * (lu**2)) / sigma_d) * 1e-9
            return SM

    def supplementary_stiffness_requirements_for_FRP(self, pressure, s, lu, cu):
        if self.craft.zone == 'Superestructura':
            resultados_I = {}
            Etc = val_data(f"Promedio del módulo de compresión y tensión ({self.craft.material}, refuerzo): ", True, True, -1, 0.001)
            kCS = self.curvature_factor_for_stiffeners_kCS(cu, lu)
            for location, pres in pressure.items():
                I = ((26 * (kCS**1.5) * pres * s * (lu**3)) / (0.05 * Etc)) * 1e-11
                resultados_I[location] = I
            return resultados_I
        else:
            kCS = self.curvature_factor_for_stiffeners_kCS(cu, lu)
            Etc = val_data(f"Promedio del módulo de compresión y tensión ({self.craft.material}, refuerzo): ", True, True, -1, 0.001)
            I = ((26 * (kCS**1.5) * pressure * s * (lu**3)) / (0.05 * Etc)) * 1e-11
            return I

    #Stiffeners requirements based on different zones
    def stiffeners(self):
        print(f"\n{self.craft.material}, refuerzos de: {self.craft.zone}\n")
        s = val_data("Separación entre refuerzos 's' (mm): ", True, True)
        lu = val_data("Longitud no soportada de refuerzos 'lu' (mm): ", True, True)
        cu = val_data("Corona o curvatura (refuerzo curvo) 'cu', sino presione Enter (mm): ", True, True, 0)
        x = val_data("Distancia desde popa a posición longitudinal del refuerzo (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        pressure = self.pressure.get_zone_pressure(b=None, l=None, s=s, lu=lu, x=x)
        
        if self.craft.material in ['Fibra laminada', 'Fibra con nucleo (Sandwich)']:
            tau = val_data(f"Resistencia al cortante mínima ({self.craft.material}, refuerzo): ", True, True, -1, 0.001)
            tau_d = 0.5 * tau
            sigma_ct = val_data(f"Esfuerzo último (compresión/tracción, {self.craft.material}, \nsegún el tipo de carga presente en el refuerzo): ", True, True, -1, 0.001)
            sigma_d = 0.5 * sigma_ct
            AW = self.web_area_AW(pressure, s, lu, tau_d)
            SM = self.min_section_modulus_SM(pressure, s, lu, cu, sigma_d)
            I = self.supplementary_stiffness_requirements_for_FRP(pressure, s, lu, cu)
            return AW, SM, I
        elif self.craft.material in ['Acero', 'Aluminio']:
            sigma_y = val_data(f"Esfuerzo de fluencia a la tracción ({self.craft.material}): ", True, True, -1, 0.001)
            tau_d = 0.45 * sigma_y if self.craft.material == 'Acero' else 0.4 * sigma_y
            sigma_d = 0.8 * sigma_y if self.craft.material == 'Acero' else 0.7 * sigma_y
            AW = self.web_area_AW(pressure, s, lu, tau_d)
            SM = self.min_section_modulus_SM(pressure, s, lu, cu, sigma_d)
            return AW, SM
        else: # Madera (laminada y plywood)
            tau = val_data(f"Resistencia al cortante mínima ({self.craft.material}, refuerzo): ", True, True, -1, 0.001)
            tau_d = 0.4 * tau
            sigma_uf = val_data(f"Esfuerzo último a la flexión ({self.craft.material}, refuerzo): ", True, True, -1, 0.001)
            sigma_d = 0.4 * sigma_uf
            AW = self.web_area_AW(pressure, s, lu, tau_d)
            SM = self.min_section_modulus_SM(pressure, s, lu, cu, sigma_d)
            return AW, SM