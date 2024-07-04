"""
                ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS
--------------------------------------------------------------------------
MATERIALS = ('Steel', 'Aluminum', 'Aluminum Extruded Planking', 'Aluminum Sandwich Panels', 'Aluminum Corrugated', 'Single Skin Laminate Fiber Plastic', 'Sandwich Laminate Fiber Plastic') 
ZONES
    # Shell:
        #1 Vagra Maestra
        #2 Bottom Shell
        #3 Side and transom Shell
    # Decks:
        #4 Strength Deck
        #5 Lower Decks/Other Decks
        #6 Wet Decks
        #7 Superstructure and deckhouses Decks 
    # Bulkheads:
        #8 Water Tight Bulkheads
        #9 Deep Tank Bulkheads
    # Others:
        #10 Superstructure and Deckhouses - Front, Sides, Ends, and Tops
        #11 Water Jet Tunnels
        #12 Transverse Thruster Tunnels/Tubes (Boat Thruster)
        #13 Decks Provided for the Operation or Stowage of Vehicles
--------------------------------------------------------------------------
MATERIALS = ('Acero', 'Aluminio', 'Aluminio extruido', 'Aluminio en Sandwich', 'Aluminio Corrugado', 'Fibra laminada', 'Fibra en sandwich') 
ZONAS
    Casco:
        1. Vagra Maestra
        2. Casco de Fondo
        3. Casco de Costado y Espejo de Popa
    Cubiertas:
        4. Cubierta Principal
        5. Cubiertas Inferiores/Otras Cubiertas
        6. Cubiertas Humedas
        7. Cubiertas de Superestructura y Casetas de Cubierta
    Mamparos:
        8. Mamparos Estancos
        9. Mamparos de Tanques Profundos
    Otros:
        10. Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos
        11. Túneles de Waterjets
        12. Túneles de Bow Thrusters
        13. Cubiertas de Operación o Almacenamiento de Vehículos
        
--------------------------------------------------------------------------
"""


import numpy as np
from validations import val_data



class Craft:
    MATERIALS = ('Acero', 'Aluminio', 'Aluminio extruido', 'Aluminio en Sandwich', 'Aluminio Corrugado', 'Fibra laminada', 'Fibra en sandwich')
    ZONES = {
        1: 'Vagra Maestra',
        2: 'Casco de Fondo',
        3: 'Casco de Costado y Espejo de Popa',
        4: 'Cubierta Principal',
        5: 'Cubiertas Inferiores/Otras Cubiertas',
        6: 'Cubiertas Humedas',
        7: 'Cubiertas de Superestructura y Casetas de Cubierta',
        8: 'Mamparos Estancos',
        9: 'Mamparos de Tanques Profundos',
        10: 'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos',
        11: 'Túneles de Waterjets',
        12: 'Túneles de Bow Thrusters',
        13: 'Cubiertas de Operación o Almacenamiento de Vehículos'
    }
    TIPO_EMBARCACION = ('Alta velocidad', 'Costera', 'Fluvial', 'Búsqueda y rescate')

    def __init__(self):
        self.designer_name = input("Diseñador: ")
        self.boat_name = input("Embarcación: ")
        self.company_name = input("Empresa: ")
        self.management_name = input("Gerencia: ")
        self.division_name = input("División: ")
        self.material = self.select_material()
        self.selected_zones = []
        self.values = {}
        

    #Metodo para pedir datos y validar si ya existe
    def get_value(self, key, prompt, *args):
        if key not in self.values:
            self.values[key] = val_data(prompt, *args)
        return self.values[key]

    #Metodo para mostrar info solo para consola
    def display_menu(self, items) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def select_tipo_embarcacion(self) -> int:
        print("\nSeleccione el tipo de embarcación")
        self.display_menu(self.TIPO_EMBARCACION)
        choice = val_data("Ingrese el número correspondiente: ", False, True, -1, 1, len(self.TIPO_EMBARCACION))
        return choice
    
    def select_material(self) -> int:
        print("\nLista de materiales disponibles")
        self.display_menu(self.MATERIALS)
        opcion = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(self.MATERIALS))
        return opcion
    
    def determine_resistencia(self) -> str: #Revisar
        if self.material == 'Acero':
            if 200 < self.sigma_y < 300:
                return 'Ordinaria'
            elif 300 <= self.sigma_y:
                return 'Alta'
            else:
                return 'Baja'
        else:
            return 'Ordinaria'
        
    def select_zones(self) -> list:
        print("\nSeleccione las zonas que desea escantillonar (ingrese '0' para finalizar) \n")
        # Mostrar las zonas desde el diccionario
        for number, name in self.ZONES.items():
            print(f"{number}. {name}")

        selected_zones = []
        while True:
            try:
                choice = val_data("Ingrese el número correspondiente y presione Enter: ", False, False, -1, 0, max(self.ZONES.keys()))
                if choice == 0:
                    if not selected_zones:  # Intenta finalizar sin seleccionar ninguna zona
                        raise ValueError("Debe seleccionar al menos una zona antes de finalizar.")
                    break  # Finaliza si hay al menos una zona seleccionada
                elif choice in self.ZONES:
                    if choice in selected_zones:
                        raise ValueError("Zona ya seleccionada, elija otra.")
                    selected_zones.append(choice)
                    print(f"Añadida: {self.ZONES[choice]}")
                else:
                    print("Selección no válida, intente de nuevo.")
            except ValueError as e:
                print(e)
 
        return selected_zones

    def get_L(self):
        return self.get_value('L', "Eslora del casco (metros): ")

    def get_LW(self):
        L = self.get_L()  # Asegura que L es obtenido y validado primero
        return self.get_value('LW', "Eslora de flotación (metros): ", True, True, -1, 0, L)

    def get_B(self):
        return self.get_value('B', "Manga Total (metros): ")

    def get_BW(self):
        B = self.get_B()  # Asegura que B es obtenido y validado primero
        return self.get_value('BW', "Manga de flotación (metros): ", True, True, -1, 0, B)

    def get_D(self):
        return self.get_value('D', "Puntal (metros): ")

    def get_d(self):
        L = self.get_L()
        D = self.get_D()
        return self.get_value('d', "Calado (metros): ", True, True, 0, 0.04 * L, D)

    def get_V(self):
        L = self.get_L()
        return self.get_value('V', "Velocidad maxima (nudos): ", True, True, -1, 0, 20 if L > 61 else None)

    def get_W(self):
        return self.get_value('W', "Desplazamiento de la embarcación (kg): ")

    def get_Bcg(self):
        return self.get_value('Bcg', "Ángulo de astilla muerta fondo en LCG (°grados): ")

    def get_tau(self):
        return self.get_value('tau', "Ángulo de trimado a velocidad máxima (grados): ", True, True, -1, 3)
    
    
class Pressures:


    def __init__(self, craft: Craft):
        self.craft = craft
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        self.h13 = self.calculate_h13()
        self.H = max(0.0172 * self.craft.L + 3.653, self.h13)
        self.Hs = max(0.083 * self.craft.L * self.craft.d, self.craft.D + 1.22) if self.craft.L < 30 else (0.64 * self.H + self.craft.d)


    def calculate_pressures(self, context, zone, l, s) -> float:
        #Se calcula la presión dependiedno de la zona
        index = None
        
        if zone == 2:  # Casco de Fondo
            x, y, Bx = self.calculate_x_y_Bx(zone)
            ncgx = self.calculate_ncgx(x)
            FD = self.calculate_FD(context, l, s)
            FV = self.calculate_FV(x)

            if self.craft.L >= 61:
                if x is None:
                    slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * FD
                else:  # x is not None
                    slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * ((70 - self.craft.Bcg) / 70) * FD
            else:  # self.craft.L < 61
                slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * FD * FV

            hidrostatic_pressure = self.N3 * (0.64 * self.H + self.craft.d)

            index = slamming_pressure > hidrostatic_pressure
            pressure = max(slamming_pressure, hidrostatic_pressure)

        elif zone == 3:  # Casco de Costado y Espejo de Popa
            x, y, Bx = self.calculate_x_y_Bx(zone)
            ncgx = self.calculate_ncgx(x)
            FD = self.calculate_FD(context, l, s)
            
            if x is None:
                slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * FD
                hidrostatic_pressure = self.N3 * self.Hs
            else:
                slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * ((70 - Bx) / (70 - self.craft.Bcg)) * FD
                hidrostatic_pressure = self.N3 * (self.Hs - y)

            # Fore End
            fore_end = None
            if self.craft.L >= 30:
                Fa = 3.25 if context == 'Plating' else 1
                Cf = 0.0125 if self.craft.L < 80 else 1.0
                # MOSTRAR IMAGEN 1
                alfa = val_data("Ángulo de ensanchamiento (grados): ")
                beta = val_data("Ángulo de entrada (grados): ")
                fore_end = 0.28 * Fa * Cf * self.N3 * (0.22 + 0.15 * np.tan(alfa)) * ((0.4 * self.craft.V * np.cos(beta) + 0.6 * self.craft.L ** 0.5) ** 2)

            index = slamming_pressure > hidrostatic_pressure
             
            if self.craft.L < 30:
                pressure = max(slamming_pressure, hidrostatic_pressure)
            else:
                pressure = max(slamming_pressure, hidrostatic_pressure, fore_end)

        elif zone == 4: #Cubierta Principal
            pressure = 0.20 * self.craft.L + 7.6

        elif zone == 5: #Cubiertas Inferiores/Otras Cubiertas
            pressure = 0.10 * self.craft.L + 6.1

        elif zone == 6: #Cubiertas Humedas
            x, y, Bx = self.calculate_x_y_Bx(zone)
            F1 = self.calculate_F1(x)
            FD = self.calculate_FD(context, l, s)
            # Mostrar imagen 2
            ha = val_data("Altura desde la línea de flotación hasta la cubierta humeda en cuestión (metros): ", True, True, 0, 0, self.craft.D - self.craft.d)
            if self.craft.L < 61:
                v1 = ((4 * self.h13) / (np.sqrt(self.craft.L))) + 1
                pressure = 30 * self.N1 * FD * F1 * self.craft.V * v1 * (1 - 0.85 * ha / self.h13)
            else:
                v1 = 5 * np.sqrt(self.h13 / self.craft.L) + 1
                pressure = 55 * FD * F1 * np.pow(self.craft.V, 0.1) * v1 * (1 - 0.35 * (ha / self.h13))

        elif zone == 7: #Cubiertas de Superestructura y Casetas de Cubierta
            pressure = 0.10 * self.craft.L + 6.1

        elif zone == 8: #Mamparos Estancos
            #Mostrar Imagen 3 - ISO 12215-5
            h = val_data("Altura del mamparo (metros): ")
            pressure = self.N3 * h
    
        elif zone == 9: #Mamparos de Tanques Profundos #Insertar Imagen
            x, y, Bx = self.calculate_x_y_Bx(zone)
            ncgx = self.calculate_ncgx(x)
            #Mostrar Imagen 3 - ISO 12215-5
            hb = val_data("Altura de la columna de agua (metros): ") 
            pg = max(10.05, val_data("Peso especifico del liquido (kN/m^3): ", True, True, -1, 0, 10.05))
            pressure_1 = self.N3 * hb
            pressure_2 = pg * (1 + 0.5 * ncgx) * hb
            pressure = max(pressure_1, pressure_2)

        elif zone == 10: #Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos
            """
            A superstructure is an enclosed structure above the freeboard deck having side plating as an extension of
            the shell plating, or not fitted inboard of the hull side more than 4% of the breadth B.

            Una superestructura es una estructura cerrada situada por encima de la cubierta de francobordo que tiene 
            una chapa lateral como prolongación de la chapa del forro exterior, o que no está instalada en el interior 
            del costado del casco más del 4% de la manga.
            """
            if context == 'Plating':
                pressures = {
                    "Chapado a proa de superestructuras y casetas": (24.1, 37.9),
                    "Chapado a popa y costados de superestructuras y casetas": (10.3, 13.8),
                    "Chapado de los techos que están en la proa": (6.9, 8.6),
                    "Chapado de los techos que están en la popa": (3.4, 6.9)
                }
            else:  # Stiffeners
                pressures = {
                    "Refuerzos delanteros de la superestructura y caseta": (24.1, 24.1),
                    "Refuerzos traseros de la superestructura y caseta, y refuerzos laterales de la caseta": (10.3, 10.3),
                    "Refuerzos de los techos que están en la proa": (6.9, 8.6),
                    "Refuerzos de los techos que están en la popa": (3.4, 6.9)
                }

            # Inicialización del diccionario de resultados
            result = {}

            # Cálculo de la presión según la longitud de la embarcación
            for location, (P1, P2) in pressures.items():
                if self.craft.L <= 12.2:
                    result[location] = P1
                elif self.craft.L > 30.5:
                    result[location] = P2
                else:
                    result[location] = np.interp(self.craft.L, [12.2, 30.5], [P1, P2])
                    
            #Retorna un diccionario
            pressure = result

        elif zone == 11: #Túneles de Waterjets #REVISAR
            index = False #REVISAR
            pressure = val_data("Presión máxima positiva o negativa de diseño del túnel [kN/m^2]: ", True, True, -1)
 
        else: #zone in [1, 12, 13]:
            pressure = "No aplica"

        return pressure, index

    def calculate_x_y_Bx(self, zone) -> tuple:
        ask = val_data(f"¿Desea realizar el análisis en algún punto específico de la zona: {self.craft.ZONES[zone]}, 0 = No, 1 = Si ?\n", False, False, 0, 0, 1)
        
        if ask == 1:
            x = val_data("Distancia desde proa hasta el punto de análisis (metros): ", True, True, -1, 0, self.craft.L)
            x = x / self.craft.L
            
            if zone == 2:
                return x, None, None
            elif zone == 3:
                y = val_data("Altura sobre la linea base hasta el punto de análisis (metros): ", True, True, 0, 0, self.craft.D)
                Bx = val_data("Ángulo de astilla muerta de costado en el punto de análisis (grados): ", True, True, -1, 0, 55)
                return x, y, Bx

        return None, None, None  # Si el usuario no desea análisis específico o la zona no requiere análisis específico
    
    def calculate_h13(self) -> float: #Revisar
        h13_values = {1: 4, 2: 2.5, 3: 0.5}
        h13 = max(h13_values.get(self.craft.tipo_embarcacion), (self.craft.L / 12))
        return h13

    def calculate_ncgx(self, x) -> float:
        kn = 0.256
        ncgx_limit = 1.39 + kn * (self.craft.V / np.sqrt(self.craft.L))
        _ncgx = self.N2 * (((12 * self.h13) / self.craft.BW) + 1) * self.craft.tau * (50 - self.craft.Bcg) * ((self.craft.V ** 2 * self.craft.BW ** 2) / self.craft.W)
        ncgx = min(ncgx_limit, _ncgx)
        if self.craft.V > (18 * np.sqrt(self.craft.L)):
            ncgx = 7 if self.craft.tipo_embarcacion == 4 else 6
        if self.craft.L < 24 and ncgx < 1:
            ncgx = 1

        # Ajuste de ncgx basado en x
        if x is not None:
            x_known = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            y_known = [0.8, 0.8, 0.8, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
            Kv = np.interp(x, x_known, y_known)
            ncgx = ncgx * Kv

        return ncgx

    def calculate_FD(self, context, l, s) -> float:
        AR = 6.95 * self.craft.W / self.craft.d

        x_known = [0.001, 0.005, 0.010, 0.05, 0.100, 0.500, 1]
        y_known = [1, 0.86, 0.76, 0.47, 0.37, 0.235, 0.2]
        
        if context == "Plating":
            AD = min(s * l, 2.5 * pow(s, 2))
            ADR = AD / AR
        else:
            AD = max(s * l, 0.33 * pow(l, 2))
            ADR = AD / AR

        FD = np.interp(ADR, x_known, y_known)
        FD = min(max(FD, 0.4), 1.0)
        
        return FD

    def calculate_FV(self, x) -> float:
        if x is None:
            return 1.0
        x_known = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.445, 0.4, 0.3, 0.2, 0.1, 0]
        y_known = [0.25, 0.39, 0.52, 0.66, 0.8, 0.92, 1, 1, 1, 1, 1, 0.5]
        FV = np.interp(x, x_known, y_known)
        return min(max(FV, 0.25), 1.0)

    def calculate_F1(self, x) -> float:
        if x is None:
            return 1.0
        x_known = [0, 0.2, 0.7, 0.8, 1.0]
        y_known = [0.5, 0.4, 0.4, 1.0, 1.0]
        return np.interp(x, x_known, y_known)

    #PARA UN POSTERIOR DESARROLLO:

    # def decks_pressures(self): 
    #     """ Las diferentes cubiertas posibles están enumeradas """
    #     cubiertas_proa = 0.20 * self.craft.L +7.6                                                   #1
    #     cubiertas_popa = 0.10 * self.craft.L + 6.1                                                  #2
    #     cubiertas_alojamientos = 5                                                                  #3     
    #     carga = val_data("Carga en la cubierta (kN/m^2): ", True, True, -1)                         
    #     cubiertas_carga = carga * (1 + 0.5 * self.nxx)                                              #4
    #     cargo_density = max(val_data("Densidad de la carga (kN/m^3): ", True, True, -1), 7.04)      
    #     height = val_data("Altura del almacén (metros): ", True, True, -1)
    #     almacenes_maquinaria_otros = cargo_density * height * (1 + 0.5 * self.nxx)                  #5

#Clases por materiales
class Acero_Aluminio_Alextruido_AlCorrugated:


    def __init__(self, craft: Craft):
        self.craft = craft
        zone_results = {}

    
    def lateral_loading(self, s, pressure, k, sigma_a) -> float:
        return s * 10 * np.sqrt((pressure * k)/(1000 * sigma_a))
    
    def secondary_stiffening(self, s) -> float:
        if self.craft.material == "Acero":
            return 0.01 * s
        else:
            return 0.012 * s
        
    def minimum_thickness(self, zona, resistenci, sigma_y) -> float:
        if self.craft.material == 'Acero':
            q = 1.0 if resistencia == "Alta" else 245 / sigma_y
        else:
            q = 115 / sigma_y
        
        if zone == 2:    #Fondo
            if self.craft.material == "Acero":
                return max(0.44 * np.sqrt(self.craft.L * q) + 2, 3.5)
            else:
                return max(0.70 * np.sqrt(self.craft.L * q) + 1, 4.0)
        elif zone == 3:  #Costados y Espejo
            if self.craft.material == "Acero":
                return max(0.40 * np.sqrt(self.craft.L * q) + 2, 3.0)
            else:
                return max(0.62 * np.sqrt(self.craft.L * q) + 1, 3.5)
        elif zone == 4:  # Strength Deck - Cubierta principal
            if self.craft.material == "Acero":
                return max(0.40 * np.sqrt(self.craft.L * q) + 1, 3.0)
            else:
                return max(0.62 * np.sqrt(self.craft.L * q) + 1, 3.5)
        else: #zone in [4, 7, 8]:  #Lower Decks, W.T. Bulkheads, Deep Tank Bulkheads
            if self.craft.material == "Acero":
                return max(0.35 * np.sqrt(self.craft.L * q) + 1, 3.0)
            else:
                return max(0.52 * np.sqrt(self.craft.L * q) + 1, 3.5)


class Aluminio_Sandwich:
    
    
    def __init__(self):
        pass
    
    
    def section_modulus_skins(self, s, pressure, k, sigma_a) -> float:
        SM = (s**2 * pressure * k) / (6e5 * sigma_a)
        return SM
    
    def moment_inertia_skins(self, s, pressure, k1, E) -> float:
        I = (s**3 * pressure * k1) / (120e5 * 0.24 * E)
        return I
    
    def core_shear_strength(self, v, pressure, s, tau) -> float:
        #core_shear:=(do + dc) / 2     #do = thickness of skins, dc = thickness of core
        core_shear = (v * pressure * s) / tau     #The thickness of core and sandwich is to be not less than given by the following equation
        return core_shear


class Fibra_Laminada:
    
    
    def __init__(self):
        pass
    
    
    #With Essentially Same Properties in 0° and 90° Axes
    def all_plating_a(self, pressure, s, c, k, sigma_a) -> float:
        t = s * c * np.cbrt((pressure * k) / (1000 * sigma_a))
        return t
    
    def all_plating_b(self, pressure, s, c, k1, k2, Ef) -> float:
        t = s * c *  np.cbrt((pressure * k1) / (1000 * k2 * Ef))
        return t
    
    def strength_deck_shell(self, c1, q1, k3, L) -> float:
        t = k3 * (c1 + 0.26 * L) * np.sqrt(q1)
        return t
    
    def strength_deck_bottom_shell(self, s, kb, uc, Ec, SM_R, SM_A) -> float:
        t = (s/kb) * np.sqrt((0.6 * uc) / Ec) * np.sqrt(SM_R / SM_A)
        return t
    
    #With Different Properties in 0° and 90° Axes
    def equation_a(self, pressure, s, c, ks, sigma_as) -> float:
        t = s * c * np.sqrt((pressure * ks) / (1000 * sigma_as))
        return t
    
    def equation_b(self, pressure, s, c, kl, sigma_al, El, Es) -> float:
        t = s * c * np.sqrt((pressure * kl) / (1000 * sigma_al)) * np.power(El / Es, 1/4)
        return t
    
    
class Fibra_Sandwich:
    
    
    def __init__(self):
        pass
    
    
    #Laminate with Essentially Same Bending Strength and Stiffness in 0° and 90° Axes
    def section_modulus_outer_skin(self, pressure, s, c, k, sigma_ao) -> float:
        SM_o = ((s * c)**2 * pressure * k) / (6e5 * sigma_ao)
        return SM_o
    
    def section_modulus_inner_skin(self, pressure, s, c, k, sigma_ai) -> float:
        SM_i = ((s * c)**2 * pressure * k) / (6e5 * sigma_ai)
        return SM_i
    
    def moment_intertia(self, pressure, s, c, k1, k2, Etc) -> float:
        I = ((s * c)**3 * pressure * k1) / (120e5 * k2 * Etc)
        return I
    
    #Laminates with Different Bending Strength and Stiffness in 0° and 90° Axes
    def section_modulus_outer_skin_parrallel_s(self, pressure, s, c, ks, sigma_aso) -> float:
        SM_o = ((s * c)**2 * pressure * ks) / (6e5 * sigma_aso)
        return SM_o
    
    def section_modulus_outer_skin_parallel_l(self, pressure, s, c, kl, sigma_alo, El, Es) -> float:
        SM_o = ((s * c)**2 * pressure * kl) / (6e5 * sigma_alo) * np.sqrt(El / Es)
        return SM_o
    
    def section_modulus_inner_skin_parrallel_s(self, pressure, s, c, ks, sigma_asi) -> float:
        SM_i = ((s * c)**2 * pressure * ks) / (6e5 * sigma_asi)
        return SM_i
    
    def section_modulus_inner_skin_parallel_l(self, pressure, s, c, kl, sigma_ali, El, Es) -> float:
        SM_i = ((s * c)**2 * pressure * kl) / (6e5 * sigma_ali) * np.sqrt(El / Es)
        return SM_i
    
    def moment_intertia_parrallel_s(self, pressure, s, c, k1, k2, Es) -> float:
        I = ((s * c)**2 * pressure * k1) / (120e5 * k2 * Es)
        return I
    
    def moment_intertia_parallel_l(self, pressure, s, c, k1, k2, El) -> float: #REVISAR LA HICE YO
        I = ((s * c)**2 * pressure * k1) / (120e5 * k2 * El)
        return I
    
    def core_shear_strength(self, v, pressure, s, tau) -> float:
        #core_shear: (do + dc) / 2 = (v * pressure * s) / 1000 * tau    #do = thickness of skins, dc = thickness of core
        core_shear = (v * pressure * s) / 1000 * tau     #The thickness of core and sandwich is to be not less than given by the following equation
        return core_shear
    
