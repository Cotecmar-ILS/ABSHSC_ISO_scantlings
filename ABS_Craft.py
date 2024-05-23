# Bottom Shell
# Side Shell
# Strenght Deck and other Decks
# Superstructure and Deckhouses – Front, Sides, Ends, and Tops
# Tank Bulkheads
# Watertight Bulkheads
# Water Jet Tunnels


import math
import numpy as np
from validations import val_data


class Craft:


    MATERIALS = ('Acero', 'Aluminio', 'Fibra laminada', 'Fibra en sandwich')
    ZONES = ('Fondo', 'Costado', 'Cubierta Principal', 'Mamparos Estancos y de Tanques', 'Superestructura y Casetas', 'Vagra Maestra')
    TIPO_EMBARCACION = ('Alta velocidad', 'Costera', 'Fluvial', 'Busqueda y rescate')

    def __init__(self):
        print("\nEscantillonados ABS Highspeed Craft --- ABS Highspeed Craft Scantlings\n")
        self.L = val_data("Eslora del casco (metros): ")
        self.LW = val_data("Eslora de flotación (metros): ")
        self.B = val_data("Manga Total (metros): ")
        self.BW = val_data("Manga de flotación (metros): ")
        self.D = val_data("Puntal (metros): ")
        self.d = val_data("Calado (metros): ")
        self.V = val_data("Velocidad maxima (nudos): ")
        self.W = val_data("Desplazamiento de la embarcación (kg): ")
        self.Bcg = val_data("Ángulo de astilla muerta fondo en LCG (°grados): ")
        self.material = self.select_material()
        self.context = self.select_context()
        self.zone = self.select_zone()
        self.sigma_u = val_data("Esfuerzo ultimo a la tracción (MPa): ")
        self.sigma_y = val_data("Limite elastico por tracción (MPa): ")
        self.resistencia = self.determine_resistencia()
        self.tipo_embarcacion = self.select_tipo_embarcacion()

    def display_menu(self, items) -> None:  #Función para mostrar el menú en consola
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def select_material(self) -> int:
        print("\nLista de materiales disponibles")
        self.display_menu(self.MATERIALS)
        opcion = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(self.MATERIALS))
        return opcion

    def select_context(self) -> int:    #Revisar esta función
        print("\n1. Chapado \
               \n2. Refuerzos")
        opcion = val_data("\nIngrese el número correspondiente al analisis: ", False, True, -1, 1, len(self.ZONES))
        return opcion

    def determine_resistencia(self) -> str:
        if self.material == 'Acero':
            if 200 < self.sigma_y < 300:
                return 'Ordinaria'
            elif 300 <= self.sigma_y:
                return 'Alta'
            else:
                return 'Baja'
        else:
            return 'Ordinaria'

    def select_zone(self) -> int:
        print("\nSeleccione la zona que desea escantillonar")
        self.display_menu(self.ZONES)
        choice = val_data("Ingrese el número correspondiente: ", False, True, -1, 1, len(self.ZONES))
        return choice

    def select_tipo_embarcacion(self) -> int:
        print("\nSeleccione el tipo de embarcación")
        self.display_menu(self.TIPO_EMBARCACION)
        choice = val_data("Ingrese el número correspondiente: ", False, True, -1, 1, len(self.TIPO_EMBARCACION))
        return choice


class Pressures:


    def __init__(self, craft: Craft):
        self.craft = craft
        self.Fx, self.y = self.calculate_Fx_y()
        self.FD = self.calculate_FD()
        self.FV = self.calculate_FV()
        self.F1 = self.calculate_F1()
        self.ncg, self.nxx, self.h13 = self.calculate_ncg_nxx_h13()
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        self.H = max(0.0172 * self.craft.L + 3.653, self.h13)
        self.Hs = max(0.083 * self.craft.L * self.craft.d, self.craft.D + 1.22) if self.craft.L < 30 else (0.64 * self.H + self.craft.d)
        self.tau = val_data("Ángulo de trimado a velocidad máxima (grados): ", True, True, -1, 3)


    def calculate_Fx_y(self) -> tuple: #Esta función solo se realiza si el usuario desea realizar el analisis en un punto especifico
        print("¿Desea realizar el análisis en algún punto específico?\n")
        lx = val_data("Distancia desde proa hasta el punto de análisis (metros): ", True, True, self.craft.L * 0.1, 0, self.craft.L)
        Fx = lx / self.craft.L
        
        #Altura sobre la linea base hasta el punto de analisis
        y = val_data("Altura sobre la linea base hasta el punto de analisis (metros): ", True, True, 0, 0, self.craft.D)
        
        return Fx, y

    def calculate_ncg_nxx_h13(self) -> tuple:
        #Calculo de h13
        h13_values = {1: 4, 2: 2.5, 3: 0.5}
        h13 = max(h13_values.get(self.craft.tipo_embarcacion), (self.craft.L / 12))

        #Calculo de ncg
        kn = 0.256
        ncg_limit = 1.39 + kn * (self.craft.V / math.sqrt(self.craft.L))
        _ncg = self.N2 * (((12 * h13) / self.craft.BW) + 1) * self.tau * (50 - self.craft.Bcg) * ((self.craft.V ** 2 * self.craft.BW ** 2) / self.craft.W)
        ncg = min(ncg_limit, _ncg)
        if self.V > (18 * math.sqrt(self.L)):
            ncg = 7 if self.craft.tipo_embarcacion == 4 else 6
        if self.L < 24 and ncg < 1:
            ncg = 1

        #Calculo de nxx
        x_known = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        y_known = [0.8, 0.8, 0.8, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        Kv = np.interp((self.craft.L - self.Fx), x_known, y_known)
        nxx = Kv * ncg
        
        return ncg, nxx, h13

    def calculate_FD(self) -> float:
        AR = 6.95 * self.craft.W / self.craft.d

        if self.craft.context == 1:
            AD = min(self.s * l, 2.5 * pow(s, 2))
        else:
            AD = max(self.s * l, 0.33 * pow(l, 2))
        ADR = AD / AR

        x_known = [0.001, 0.005, 0.010, 0.05, 0.100, 0.500, 1]
        y_known = [1, 0.86, 0.76, 0.47, 0.37, 0.235, 0.2]
        FD = np.interp(ADR, x_known, y_known)

        FD = min(max(FD, 0.4), 1.0)

        return FD

    def calculate_FV(self) -> float:
        x_known = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.445, 0.4, 0.3, 0.2, 0.1, 0]
        y_known = [0.25, 0.39, 0.52, 0.66, 0.8, 0.92, 1, 1, 1, 1, 1, 0.5]
        FV = np.interp(self.Fx, x_known, y_known)
        FV = min(max(FV, 0.25), 1.0)

        return FV

    def calculate_F1(self) -> float:
        x_known = [0, 0.2, 0.7, 0.8, 1.0]
        y_known = [0.5, 0.4, 0.4, 1.0, 1.0]
        F1 = np.interp(self.Fx, x_known, y_known)

        return F1

    def bottom_pressure(self) -> float:
        slamming_pressure_less61 = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + self.ncg) * self.FD * self.FV)
        hidrostatic_pressure = self.N3 * (0.64 * self.H + self.craft.d)
        return max (slamming_pressure_less61, hidrostatic_pressure)

    def side_transom_pressure(self):
        #Ángulo de astilla muerta en el punto de análisis
        Bsx = val_data("Angulo de astilla muerta de costado en el punto de analisis (grados): ", True, True, -1, 0, 55)
        slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + self.nxx) * ((70 - Bsx) / (70 - self.craft.Bcg)) * self.FD
        hidrostatic_pressure = self.N3 * (self.Hs - self.y)

        #Fore End
        if self.craft.L >= 30:
            Fa = 3.25 if self.craft.context == 1 else 1
            Cf = 0.0125 if self.craft.L < 80 else 1.0
            alfa = val_data("Ángulo de ensanchamiento (grados): ") #Ver imagen adjunta
            beta = val_data("Ángulo de entrada (grados): ") #Ver imagen adjunta
            fore_end = 0.28 * Fa * Cf * self.N3 * (0.22 + 0.15 * np.tan(alfa)) * ((0.4 * self.craft.V * np.cos(beta) + 0.6 * self.craft.L ** 0.5) ** 2)

        return max(slamming_pressure, hidrostatic_pressure) if self.craft.L < 30 else max(slamming_pressure, hidrostatic_pressure), fore_end

    def wet_deck_pressure(self):
        ha = val_data("Altura desde la línea de flotación hasta la cubierta humeda en cuestión (metros): ", True, True, 0, 0, self.craft.D - self.craft.d)

        if self.craft.L < 61:
            v1 = ((4 * self.h13) / (np.sqrt(self.craft.L))) + 1
            deck_pressure = 30 * self.N1 * self.FD * self.F1 * self.craft.V * v1 * (1 - 0.85 * ha / self.h13)
        else:
            #V is not to be greater than 20 knots for craft greater than 61 meters
            v1 = 5 * np.sqrt(self.h13 / self.craft.L) + 1
            deck_pressure = 55 * self.FD * self.F1 * np.pow(self.craft.V, 0.1) * v1 * (1 - 0.35 * (ha / self.h13))

        return deck_pressure

    #De aqui para abajo las zonas son opcionales para el usuario
    #Se debe hacer una checklist con las zonas que el usuario desee antes de realizar el analisis
    def decks_pressures(self):
        """ Las diferentes cubiertas posibles están enumeradas """
        cubiertas_proa = 0.20 * self.craft.L +7.6                                                   #1
        cubiertas_popa = 0.10 * self.craft.L + 6.1                                                  #2
        cubiertas_alojamientos = 5                                                                  #3     
        carga = val_data("Carga en la cubierta (kN/m^2): ", True, True, -1)                         
        cubiertas_carga = carga * (1 + 0.5 * self.nxx)                                              #4
        cargo_density = max(val_data("Densidad de la carga (kN/m^3): ", True, True, -1), 7.04)      
        height = val_data("Altura del almacén (metros): ", True, True, -1)
        almacenes_maquinaria_otros = cargo_density * height * (1 + 0.5 * self.nxx)                  #5

    def superstructures_pressures(self):
        plating_pressures = {
            "Chapado a proa de superestructuras y casetas": (24.1, 37.9),
            "Chapado a popa y costados de superestructuras y casetas": (10.3, 13.8),
            "Chapado de los techos que están en al proa": (6.9, 8.6),
            "Chapado de los techos que estánen la popa": (3.4, 6.9)
        }

        stiffeners_pressures = {
            "Refuerzos delanteros de la superestructura y caseta": (24.1, 24.1),
            "Refuerzos traseros de la superestructura y caseta, y refuerzos laterales de la caseta": (10.3, 10.3),
            "Refuerzos de los techos que están en la proa": (6.9, 8.6),
            "Refuerzos de los techos que están en la popa": (3.4, 6.9)
        }

        result = {}

        if self.craft.context == 1:
            pressures = plating_pressures
        else:
            pressures = stiffeners_pressures

        for location, (P1, P2) in pressures.items():
            if self.craft.L <= 12.2:
                result[location] = P1
            elif self.craft.L > 30.5:
                result[location] = P2
            else:
                result[location] = np.interp(self.craft.L, [12.2, 30.5], [P1, P2])

        return result

    def tank_boundaries_pressure(self):
        h = None
        pressure_1 = self.N3 * h
        pg = max(10.05, val_data("Peso especifico del liquido: "))
        h2 = val_data("Distancia desde el borde inferior del panel de chapa o el centro de la zona soportada por el refuerzo hasta la parte superior del depósito (metros): ")
        pressure_2 = pg * (1 + 0.5 * self.nxx) * h2
        tank_pressure = max(pressure_1, pressure_2)

        return tank_pressure    

    def watertight_boundaries_pressure(self):
        h = val_data("Distancia desde el borde inferior del panel de chapa o el centro del área soportada por el refuerzo hasta la cubierta de cierre en la línea central (metros): ")
        watertight_pressure = self.N3 * h

        return watertight_pressure


class Plating_acero_aluminio:


    def __init__(self, craft: Craft, pressure: Pressures):
        self.craft = craft
        self.pressure = pressure
        self.k = self.calculate_k_k1()[0] if self.craft.material in ['Acero', 'Aluminio'] else self.calculate_k_k1()[1]
        self.q = self.calculate_q()


    def calculate_k_k1(self) -> tuple:
        ls_known = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        k_known = [0.308, 0.348, 0.383, 0.412, 0.436, 0.454, 0.468, 0.479, 0.487, 0.493, 0.500]
        k1_known = [0.014, 0.017, 0.019, 0.021, 0.024, 0.024, 0.025, 0.026, 0.027, 0.027, 0.028]

        ls = self.l / self.s

        if ls > 2.0:
            k = 0.500
            k1 = 0.028
        elif ls < 1.0:
            k = 0.308
            k1 = 0.014
        else:
            k = np.interp(ls, ls_known, k_known)
            k1 = np.interp(ls, ls_known, k1_known)

        return k, k1

    def calculate_q(self) -> float:
        if self.craft.material == 'Acero':
            return 1.0 if self.craft.resistencia == "Alta" else 245 / self.sigma_y
        else:
            return 115 / self.sigma_y

    def design_stress(self): #revisar
        """
            Calcula el esfuerzo de diseño 'sigma_a' basado en la zona seleccionada.
            En las cubiertas y los mamparos no hay Slamming ni Hydrostatic pressure,
            solo una para ambos.

            Notes:

            1 sigma_y = yield strength of steel or of welded aluminum in N/mm2, but not to be taken 
            greater than 70% of the ultimate strength of steel or welded aluminum

            2 The design stress for bottom shell plates under slamming pressure may be taken as 
            sigma_y for plates outside the midship 0.4L.

            3 The design stress for steel deckhouse plates may be taken as 0.90 * sigma_y
        """

        if self.craft.zone == 1:    #Bottom
            Slamming_Pressure = 0.90 * self.sigma_y,
            Hydrostatic_Pressure = 0.55 * self.sigma_y,
        elif self.craft.zone == 2:  #Side
            Slamming_Pressure = 0.90 * self.sigma_y,
            Hydrostatic_Pressure = 0.55 * self.sigma_y,
        elif self.craft.zone == 3:  #Decks
            all_decks = 0.60 * self.sigma_y,
            wet_decks =0.90 * self.sigma_y,
        elif self.craft.zone == 4:  #Bulkheads
            deep_tank = 0.60 * self.sigma_y,
            watertight = 0.95 * self.sigma_y,
        elif self.craft.zone == 5:  #Superstructure
            super_deckhouse = 0.60 * self.sigma_y,
        else:   #Water Jet Tunnels
            Slamming_Pressure = 0.60 * self.sigma_y,
            Hydrostatic_Pressure = 0.55 * self.sigma_y

    #The thickness of the shell, deck or bulkhead plating
    def lateral_loading(self) -> float:
        t1 = self.s * 10 * math.sqrt((self.pressure * self.k)/(1000*self.d_stressp))
        return t1

    def secondary_stiffening(self) -> float:
        if self.craft.material == "Acero":
            return 0.01 * self.s
        else:
            return 0.012 * self.s

    def minimun_thickness(self) -> float:

        if self.craft.zone == 1:    #Fondo
            if self.craft.material == "Acero":
                return max(0.44 * math.sqrt(self.craft.L * self.q) + 2, 3.5)
            else:
                return max(0.70 * math.sqrt(self.craft.L * self.q) + 1, 4.0)
        elif self.craft.zone == 2:  #Costados y Espejo
            if self.craft.material == "Acero":
                return max(0.40 * math.sqrt(self.craft.L * self.q) + 2, 3.0)
            else:
                return max(0.62 * math.sqrt(self.craft.L * self.q) + 1, 3.5)
        elif self.craft.zone == 3:  #Cubierta principal
            if self.craft.material == "Acero":
                return max(0.40 * math.sqrt(self.craft.L * self.q) + 1, 3.0)
            else:
                return max(0.62 * math.sqrt(self.craft.L * self.q) + 1, 3.5)
        elif self.craft.zone == 4:  #Lower Decks, W.T. Bulkheads, Deep Tank Bulkheads
            if self.craft.material == "Acero":
                return max(0.35 * math.sqrt(self.craft.L * self.q) + 1, 3.0)
            else:
                return max(0.52 * math.sqrt(self.craft.L * self.q) + 1, 3.5)

    #Water Jet Tunnels
    t = self.s * np.sqrt(pressure * self.k / (1000 * self.d_stressp))

    #Transverse Thruster Tunnels/Tubes
    t = 0.008 *self.d * np.sqrt(Q) + 3.0

    #Decks Provided for the Operation or Stowage of Vehicles
    t = np.sqrt((self.beta * self.W *(1 + 0.5 * self.nxx)) / self.sigma_a)


class Internals:


    def __init__(self, craft: Craft, pressure: Pressures) -> None:
        self.craft = craft
        self.pressure = pressure


    def dstress_internals(self, zone) -> tuple:  #Corregir
        """Calcula el esfuerzo de diseño basado en la zona seleccionada."""
        zones = {
            'Fondo': {
                'Bottom Longitudinals Slamming Pressure': 0.65 * self.sigma_y,
                'Bottom Transverse and Girders Slamming pressure': 0.80 * self.sigma_y,
                'Bottom Longitudinals Sea Pressure': 0.50 * self.sigma_y,
                'Bottom Transverses and Girders Sea pressure': 0.60 * self.sigma_y
            },
            'Costado': {
                'Side Longitudinals Slamming Pressure': 0.60 * self.sigma_y,
                'Side Transverses and Girders Slamming Pressure': 0.80 * self.sigma_y,
                'Side Longitudinals Sea Pressure': 0.50 * self.sigma_y,
                'Side Transverses and Girders Sea Pressure': 0.60 * self.sigma_y,
            },
            'Cubiertas, Mamparos y Superestructura': {
                'Deck Longitudinals - Strength Decks': 0.33 * self.sigma_y,
                'Deck Longitudinals - Other Decks': 0.40 * self.sigma_y,
                'Deck Transverses and Girders Strength Decks': 0.75 * self.sigma_y,
                'Deck Transverses and Girders Other Decks': 0.75 * self.sigma_y, 
                'Wet Deck Longitudinals': 0.75 * self.sigma_y,
                'Wet Deck Transverses and Girders': 0.75 * self.sigma_y,
                'Watertight Bulkheads': 0.85 * self.sigma_y,
                'Tank Bulkheads': 0.60 * self.sigma_y,
                'Superstructure and Deckhouse': 0.70 * self.sigma_y
            },
        }
        if zone == 'Cuaderna Maestra':
            zone = 'Fondo'
        selected_zone = zones[zone]
        stress_values = tuple(selected_zone.values())
        return stress_values

    def calculate_section_modulus(self) -> float:
        SM = (83.3 * self.pressure * s * l**2) / (sigma_a)
        return SM

    def calculate_moment_inertia(self):
        I = (260 * self.pressure * s * np.pow(l, 3)) / (K4 * E)
        return I 



def main():
    pass


if __name__ == "__main__":
    main()