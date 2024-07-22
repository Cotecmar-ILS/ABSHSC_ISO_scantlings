from General import Craft
from Pressures import Pressure
from validations import val_data

class Plating():
    def __init__(self, craft: Craft, pressure: Pressure):
        self.craft = craft
        self.pressure = pressure

    def curvature_correction_kC(self, b, c):
        cb = c / b
        if cb <= 0.03:
            kC = 1.0
        elif cb <= 0.18 and cb > 0.03: #Modificado
            kC = 1.1 - (3.33 * c) / b
        else:  # cb > 0.18
            kC = 0.5
        # Aplica las restricciones de que kC no debe ser menor a 0.5 ni mayor a 1.0
        kC = max(min(kC, 1.0), 0.5)
        return kC

    #Plating equiations based on different materials
    def FRP_single_skin_plating(self, b, sigma_uf, c, k2, pressure):
        sigma_d = 0.5 * sigma_uf
        kC = self.curvature_correction_kC(b, c)
        thickness = b * kC * ((pressure * k2)/(1000 * sigma_d))**0.5
        return thickness

    def metal_plating(self, b, sigma_u, sigma_y, c,  k2, pressure):
        sigma_d = min(0.6 * sigma_u, 0.9 * sigma_y)
        kC = self.curvature_correction_kC(b, c)
        thickness = b * kC * ((pressure * k2)/(1000 * sigma_d))**0.5
        return thickness

    def wood_plating(self, b, sigma_uf, k2, pressure):
        sigma_d = 0.5 * sigma_uf
        thickness = b * ((pressure * k2)/(1000 * sigma_d))**0.5
        return thickness

    def FRP_sandwich_plating(self, b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure):
        #Note: For a sandwich the b dimension corresponds to the length of a stiffener.
        k1 = 0.017  #Bending deflection factor k1 for sandwich plating
        #Design tensile stress on the outer skin: dto
        sigma_dt = 0.5 * sigma_ut
        #Design compressive stress on the inner skin: dti
        sigma_dc = 0.5 * sigma_uc
        #Minimum required section modulus of the outer skin of sandwich 1 cm wide:
        SM_inner = ((b**0.5) * (self.curvature_correction_kC(b, c)**0.5) * pressure * k2)/(6e5 * sigma_dt)  
        #Minimum required section modulus of the inner skin of sandwich 1 cm wide:
        SM_outter = ((b**0.5) * (self.curvature_correction_kC(b, c)**0.5) * pressure * k2)/(6e5 * sigma_dc)
        #Minimum required second moment (moment of inertia) for a strip of sandwich 1 cm wide:
        second_I = ((b**3) * (self.curvature_correction_kC(b, c)**3) * pressure * k3) / (12e6 * k1 * Eio)
        if self.craft.skin[0] != self.craft.skin[1]:
            second_I = ((b**3) * (self.curvature_correction_kC(b, c)**3) * pressure * k3) / (12e3 * k1) #EI
            #This approach is better when the inner and outer faces are very different, e.g. carbon inner and carbon/aramid outer.
        if self.craft.skin[2] == 'Madera Balsa':
            tau_d = tau_u * 0.5
        elif self.craft.skin[2] == 'Núcleo con elongación al corte en rotura < 35 % (PVC entrecruzado, etc.)':
            tau_d = tau_u * 0.55
        elif self.craft.skin[2] == 'Núcleo con elongación al corte en rotura > 35 % (PVC lineal, SAN, etc.)':
            tau_d = tau_u * 0.65
        else: #self.craft.skin[2] ==  'Núcleos tipo panal de abeja (compatibles con aplicaciones marinas)':
            tau_d = tau_u * 0.5
        #Minimum design core shear according to craft length
        if self.craft.LH < 10:
            tau_d = max(tau_d, 0.25)
        elif self.craft.LH <= 10 and self.craft.LH <= 15:
            tau_d = max(tau_d, 0.25 + 0.03 * (self.craft.LH - 10))
        else:
            tau_d = max(tau_d, 0.40)
        # Shear strength aspect ratio factor kSHC
        kSHC = 0.035 + 0.394 * ar - 0.09 * ar**2 if ar < 2 else 0.5
        #Thickness required by shear load capabilities:
        thickness = (self.curvature_correction_kC(b, c)**0.5) * ((kSHC * pressure * b)/(1000 * tau_d))
        #sandwich thickness = tc + 0.5 (t i + to) is the distance between mid-thickness of the skins of the sandwich, in millimetres
        return SM_inner, SM_outter, second_I, thickness

    #Min plating (thickness)
    def min_bottom_thickness(self, sigma_y,  sigma_uf): #1 modificación
        if self.craft.material in ['Fibra laminada', 'Fibra con nucleo (Sandwich)']:
            k4 = 1.0
            if self.craft.skin == 'Fibra de vidrio E con filamentos cortados':
                k5 = 1.0
            elif self.craft.skin == 'Fibra de vidrio tejida':
                k5 = 0.9
            else: #self.craft.skin == 'Fibra tejida de carbono, aramida(kevlar) o híbrida':
                k5 = 0.7
            k6 = 1.0
            wos = self.pressure.design_category_kDC() * k4 * k5 * k6 * (0.1 * self.craft.LWL + 0.15)
            wis = 0.7 * wos
            w_min = 0.43 * k5 * (1.5 + 0.03 * self.craft.V + 0.15 * self.craft.mLDC**0.33)
            if self.craft.material == 'Fibra laminada': #Modificado
                return w_min
            else:
                return w_min, wos, wis
        elif self.craft.material == "Aluminio":
            t_min = ((125/sigma_y)**0.5) * (1 + 0.02 * self.craft.V + 0.1 * self.craft.mLDC**0.33)
        elif self.craft.material == "Acero":
            t_min = ((240/sigma_y)**0.5) * (1 + 0.015 * self.craft.V + 0.08 * self.craft.mLDC**0.33)
        elif self.craft.material == "Madera (laminada y plywood)":
            t_min = ((30/sigma_uf)**0.5) * (3 + 0.05 * self.craft.V + 0.3 * self.craft.mLDC**0.33)
        return t_min

    def min_side_transom_thickness(self, sigma_y, sigma_uf):
        if self.craft.material in ['Fibra laminada', 'Fibra con nucleo (Sandwich)']:
            k4 = 0.9
            if self.craft.skin == 'Fibra de vidrio E con filamentos cortados':
                k5 = 1.0
            elif self.craft.skin == 'Fibra de vidrio tejida':
                k5 = 0.9
            else: #self.craft.skin == 'Fibra tejida de carbono, aramida(kevlar) o híbrida':
                k5 = 0.7
            k6 = 1.0
            wos = self.pressure.design_category_kDC() * k4 * k5 * k6 * (0.1 * self.craft.LWL + 0.15)
            wis = 0.7 * wos
            w_min = 0.43 * k5 * (1.5 + 0 * self.craft.V + 0.15 * self.craft.mLDC**0.33)
            if self.craft.material == 'Fibra laminada': #Modificado
                return w_min
            else:
                return w_min, wos, wis
        elif self.craft.material == "Aluminio":
            t_min = ((125/sigma_y)**0.5) * (1 + 0 * self.craft.V + 0.1 * self.craft.mLDC**0.33)
        elif self.craft.material == "Acero":
            t_min = ((240/sigma_y)**0.5) * (1 + 0 * self.craft.V + 0.08 * self.craft.mLDC**0.33)
        elif self.craft.material == "Madera (laminada y plywood)":
            t_min = ((30/sigma_uf)**0.5) * (3 + 0 * self.craft.V + 0.3 * self.craft.mLDC**0.33)
        return t_min

    def min_deck_thickness(self):
        if self.craft.material in ['Fibra laminada', 'Fibra con nucleo (Sandwich)']:
            k4 = 0.7
            if self.craft.skin == 'Fibra de vidrio E con filamentos cortados':
                k5 = 1.0
            elif self.craft.skin == 'Fibra de vidrio tejida':
                k5 = 0.9
            else: #self.craft.skin == 'Fibra tejida de carbono, aramida(kevlar) o híbrida':
                k5 = 0.7
            k6 = 1.0
            wos = self.pressure.design_category_kDC() * k4 * k5 * k6 * (0.1 * self.craft.LWL + 0.15)
            wis = 0.7 * wos
            t_min = k5 * (1.45 + 0.14 * self.craft.LWL)
            """
            For FRP, this requirement may be translated into the 
            fibre dry mass using Equations (C.1) to (C.3).
            """
            if self.craft.material == 'Fibra laminada': #Modificado
                return t_min
            else:
                return t_min, wos, wis
        elif self.craft.material == "Aluminio":
            t = 1.35 + 0.06 * self.craft.LWL
        elif self.craft.material == "Acero":
            t = 1.5 + 0.07 * self.craft.LWL
        elif self.craft.material == "Madera (laminada y plywood)":
            t = 3.8 + 0.17 * self.craft.LWL
        return t

    #Final Thickeness for different types of zones
    def bottom_plating(self): # 1 Modificacion
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para el enchapado de: {self.craft.zone}\n") #Modificado
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        print("\nSi desea calcular el enchapado o los refuerzos en algun punto especifico digite los siguientes datos, caso contrario presione Enter")
        x = val_data("Ingrese la distancia desde la popa hasta la posición longitudinal del centro del panel o centro del refuerzo analizado (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        pressure = self.pressure.bottom_pressure(b, l, s=None, lu=None, x=x)
        
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            w_min = self.min_bottom_thickness(sigma_y=None, sigma_uf=sigma_uf)
            return t_final, w_min
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = max(self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure), self.min_bottom_thickness(sigma_y, sigma_uf=None))
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = max(self.wood_plating(b, sigma_uf, k2, pressure), self.min_bottom_thickness(sigma_y=None, sigma_uf=sigma_uf))
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            wos, wis, w_min = self.min_bottom_thickness(b, c, sigma_y=None,  sigma_uf=None)
            return t_final, SM_inner, SM_outter, second_I, wos, wis, w_min

    def side_transom_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        print("\nSi desea calcular el enchapado o los refuerzos en algun punto especifico digite los siguientes datos, caso contrario presione Enter")
        x = val_data("Ingrese la distancia desde la popa hasta la posición longitudinal del centro del panel o centro del refuerzo analizado (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        pressure = self.pressure.side_transom_pressure(b, l, s=None, lu=None, x=x)
        
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            w_min = self.min_side_transom_thickness(sigma_y=None, sigma_uf=sigma_uf)
            return t_final, w_min
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = max(self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure), self.min_side_transom_thickness(sigma_y, sigma_uf=None))
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = max(self.wood_plating(b, sigma_uf, k2, pressure), self.min_side_transom_thickness(sigma_y=None, sigma_uf=sigma_uf))
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            wos, wis, w_min = self.min_side_transom_thickness(b, c, sigma_y=None,  sigma_uf=None)
            return t_final, SM_inner, SM_outter, second_I, wos, wis, w_min 

    def deck_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2 
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        print("\nSi desea calcular el enchapado o los refuerzos en algun punto especifico digite los siguientes datos, caso contrario presione Enter")
        x = val_data("Ingrese la distancia desde la popa hasta la posición longitudinal del centro del panel o centro del refuerzo analizado (metros): ", True, True, self.craft.LWL, 0, self.craft.LWL)
        pressure = self.pressure.deck_pressure(b, l, s=None, lu=None, x=x)
        
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            t_min = self.min_deck_thickness()
            return t_final, t_min
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = max(self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure), self.min_deck_thickness())
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = max(self.wood_plating(b, sigma_uf, k2, pressure), self.min_deck_thickness())
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            wos, wis, t_min = self.min_deck_thickness()
            return t_final, SM_inner, SM_outter, second_I, wos, wis, t_min 

    def superstructures_deckhouses_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar*2) + 0.910 * ar - 0.554) / ((ar*2) - 0.313 * ar + 1.351), 0.308), 0.5)
        pressure_dict = self.pressure.superstructures_deckhouses_pressure(b, l, s=None, lu=None)
        results = {}

        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            for location, pressure in pressure_dict.items():
                t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
                results[location] = t_final
                
        elif self.craft.material in ['Acero', 'Aluminio']:
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            for location, pressure in pressure_dict.items():
                t_final = self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure)
                results[location] = t_final

        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            for location, pressure in pressure_dict.items():
                t_final = self.wood_plating(b, sigma_uf, k2, pressure)
                results[location] = t_final

        else: #self.craft.material == 'Fibra con nucleo (Sandwich)'
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar*2) - 0.029 * ar + 0.011) / ((ar*2) - 1.463 * ar + 1.108), 0.014), 0.028)
            for location, pressure in pressure_dict.items():
                SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
                results[location] = {
                'Thickness': t_final,
                'SM_Inner': SM_inner,
                'SM_Outter': SM_outter,
                'Second_Moment_of_Area': second_I
                }

        return results

    def watertight_bulkheads_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        pressure = self.pressure.watertight_bulkheads_pressure()
        
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = self.wood_plating(b, sigma_uf, k2, pressure)
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            return t_final, SM_inner, SM_outter, second_I

    def integral_tank_bulkheads_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        pressure = self.pressure.integral_tank_bulkheads_pressure()
       
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = self.wood_plating(b, sigma_uf, k2, pressure)
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            return t_final, SM_inner, SM_outter, second_I

    def wash_plates_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        pressure = self.pressure.wash_plates_pressure()
        
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = self.wood_plating(b, sigma_uf, k2, pressure)
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            return t_final, SM_inner, SM_outter, second_I

    def collision_bulkheads_plating(self):
        print(f"\nIngrese las dimensiones y las propiedades de: {self.craft.material} para: {self.craft.zone}\n")
        b = val_data("Ingrese la dimensión más corta o base del panel de la lamina 'b' (mm): ", True, True, -1, 1)
        l = val_data("Digite el lado más largo del panel de la lamina 'l' (mm): ", True, True, -1, b, 330 * self.craft.LH)
        ar = l / b
        #Panel aspect ratio factor for strength k2
        k2 = min(max((0.271 * (ar**2) + 0.910 * ar - 0.554) / ((ar**2) - 0.313 * ar + 1.351), 0.308), 0.5)
        pressure = self.pressure.collision_bulkheads_pressure()
       
        if self.craft.material == 'Fibra laminada':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material}: ")
            t_final = self.FRP_single_skin_plating(b, sigma_uf, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Acero' or self.craft.material == 'Aluminio':
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_u = val_data(f"Ingrese el esfuerzo último a la tracción del {self.craft.material}: ")
            sigma_y = val_data(f"Ingrese el esfuerzo de fluencia a la tracción del {self.craft.material}: ", True, True, -1, 0.001, sigma_u)
            t_final = self.metal_plating(b, sigma_u, sigma_y, c, k2, pressure)
            return t_final
        elif self.craft.material == 'Madera (laminada y plywood)':
            sigma_uf = val_data(f"Ingrese la resistencia ultima a la flexión de la {self.craft.material} paralela al lado corto del panel: ")
            t_final = self.wood_plating(b, sigma_uf, k2, pressure)
            return t_final
        else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
            b = min(b, 330 * self.craft.LH)
            c = val_data("Ingrese la corona o curvatura del panel 'c' (mm): ", True, True, 0)
            sigma_ut = val_data("Ingrese el esfuerzo último a la tracción de la fibra externa: ")
            sigma_uc = val_data("Ingrese el esfuerzo último a la compresión de la fibra interna: ")
            Eio = val_data("Ingrese el promedio de los módulos de Young de las caras interna y externa (MPa): ")
            tau_u = val_data("Ingrese el esfuerzo último al cortante del núcleo: ")
            k3 = min(max((0.027 * (ar**2) - 0.029 * ar + 0.011) / ((ar**2) - 1.463 * ar + 1.108), 0.014), 0.028)
            SM_inner, SM_outter, second_I, t_final = self.FRP_sandwich_plating(b, ar, c, sigma_ut, sigma_uc, Eio, tau_u, k2, k3, pressure)
            return t_final, SM_inner, SM_outter, second_I
         
        return self.pressure.transmision_pilar_loads_pressure()