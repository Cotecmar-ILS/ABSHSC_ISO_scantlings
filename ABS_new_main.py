"""
                ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS
--------------------------------------------------------------------------
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

    
    MATERIALS = ('Acero', 'Aluminio', 'Fibra laminada', 'Fibra en sandwich')
    ZONES = {1:'Vagra Maestra',
             2:'Casco de Fondo', 
             3:'Casco de Costado y Espejo de Popa',
             4:'Cubierta Principal',
             5:'Cubiertas Inferiores/Otras Cubiertas',
             6:'Cubiertas Humedas',
             7:'Cubiertas de Superestructura y Casetas de Cubierta',
             8:'Mamparos Estancos',
             9:'Mamparos de Tanques Profundos',
             10:'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos',
             11:'Túneles de Waterjets',
             12:'Túneles de Bow Thrusters',
             13:'Cubiertas de Operación o Almacenamiento de Vehículos'}
    TIPO_EMBARCACION = ('Alta velocidad', 'Costera', 'Fluvial', 'Busqueda y rescate')


    def __init__(self):
        print("\nESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS\n")
        self.L = val_data("Eslora del casco (metros): ")
        self.LW = val_data("Eslora de flotación (metros): ")
        self.B = val_data("Manga Total (metros): ")
        self.BW = val_data("Manga de flotación (metros): ")
        self.D = val_data("Puntal (metros): ")
        self.d = val_data("Calado (metros): ", True, True, 0, 0.04 * self.L)
        self.V = val_data("Velocidad maxima (nudos): ", True, True, -1, 0, 20 if self.L > 61 else None)
        self.W = val_data("Desplazamiento de la embarcación (kg): ")
        self.Bcg = val_data("Ángulo de astilla muerta fondo en LCG (°grados): ")
        self.tau = val_data("Ángulo de trimado a velocidad máxima (grados): ", True, True, -1, 3)
        self.tipo_embarcacion = self.select_tipo_embarcacion()
        self.material = self.select_material()
        self.sigma_u = val_data("Esfuerzo ultimo a la tracción (MPa): ")
        self.sigma_y = val_data("Limite elastico por tracción (MPa): ")
        self.resistencia = self.determine_resistencia()
        self.selected_zones = self.select_zones()
        
        
    def display_menu(self, items) -> None: #Funcion auxiliar para consola
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

    # def select_context(self) -> int:    #Revisar esta función
    #     print("\n1. Chapado \
    #            \n2. Refuerzos")
    #     opcion = val_data("\nIngrese el número correspondiente al analisis: ", False, True, -1, 1, len(self.ZONES))
    #     return opcion

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

    def select_zones(self) -> list:
        print("\nSeleccione las zonas que desea escantillonar (ingrese '0' para finalizar):")
        # Mostrar las zonas desde el diccionario
        for number, name in self.ZONES.items():
            print(f"{number}. {name}")

        selected_zones = []
        while True:
            try:
                choice = val_data("Ingrese el número correspondiente y presione Enter o '0' para finalizar: ", False, True, -1, 0, max(self.ZONES.keys()))
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


class Pressures:    #Tengo que identificar para que zonas l y s son requeridas


    def __init__(self, craft: Craft):
        self.craft = craft
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        self.h13 = self.calculate_h13()
        self.H = max(0.0172 * self.craft.L + 3.653, self.h13)
        self.Hs = max(0.083 * self.craft.L * self.craft.d, self.craft.D + 1.22) if self.craft.L < 30 else (0.64 * self.H + self.craft.d)


    def calculate_pressures(self, zone, l, s):
        ask = val_data(f"¿Desea realizar el análisis en algún punto específico de la zona: {self.craft.ZONES[zone]}, S/N ?\n", False, ['S', 'N'], 'N')
        if ask == 'S':
            x = val_data("Distancia desde proa hasta el punto de análisis (metros): ", True, True, self.craft.L * 0.5, 0, self.craft.L)
            lx = x / self.craft.L
        else:
            lx = 0.5
            

        if zone == 2:   #Casco de Fondo
            ncgx = self.calculate_ncgx(lx)
            FD = self.calculate_FD(l, s)
            FV = self.calculate_FV(lx)
            if self.craft.L >= 61:
                Bbx = val_data("Ángulo de astilla muerta de fondo en el punto de analisis (grados): ")
            else:
                Bbx = None
                
            if self.craft.L >= 61:
                if ncgx == False:
                    slamming_pressure = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * FD)
                else:
                    slamming_pressure = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * ((70 - Bbx) / (70 - self.craft.Bcg)) * FD)
            else: # self.craft.L < 61
                slamming_pressure = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * FD * FV)
            
            hidrostatic_pressure = self.N3 * (0.64 * self.H + self.craft.d)
            if slamming_pressure > hidrostatic_pressure:
                index = True  # True indica que es slamming
            else:
                index = False  # False indica que es hidrostatic
            pressure = max(slamming_pressure, hidrostatic_pressure), index

        elif zone == 3: #Casco de Costado y Espejo de Popa
            print(f"¿Desea realizar el análisis en algún punto específico de la zona: {self.craft.ZONES[zone]}, o presione Enter para continuar:  ?\n") #Esta función solo se realiza si el usuario desea realizar el analisis en un punto especifico
            y = val_data("Altura sobre la linea base hasta el punto de analisis (metros): ", True, True, 0, 0, self.craft.D)
            ncgx = self.calculate_ncgx(lx)
            FD = self.calculate_FD(l, s)
            
            #Ángulo de astilla muerta en el punto de análisis
            Bsx = val_data("Angulo de astilla muerta de costado en el punto de analisis (grados): ", True, True, -1, 0, 55)
            slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + ncgx) * ((70 - Bsx) / (70 - self.craft.Bcg)) * FD
            hidrostatic_pressure = self.N3 * (self.Hs - y)

            #Fore End
            if self.craft.L >= 30:
                Fa = 3.25 if self.craft.context == 1 else 1
                Cf = 0.0125 if self.craft.L < 80 else 1.0
                alfa = val_data("Ángulo de ensanchamiento (grados): ") #Ver imagen adjunta
                beta = val_data("Ángulo de entrada (grados): ") #Ver imagen adjunta
                fore_end = 0.28 * Fa * Cf * self.N3 * (0.22 + 0.15 * np.tan(alfa)) * ((0.4 * self.craft.V * np.cos(beta) + 0.6 * self.craft.L ** 0.5) ** 2)

            pressure = max(slamming_pressure, hidrostatic_pressure) if self.craft.L < 30 else max(slamming_pressure, hidrostatic_pressure), fore_end
            
        elif zone == 4: #Cubierta Principal
            pressure = 0.20 * self.craft.L + 7.6
            
        elif zone == 5: #Cubiertas Inferiores/Otras Cubiertas
            pressure = 0.10 * self.craft.L + 6.1
            
        elif zone == 6: #Cubiertas Humedas
            F1 = self.calculate_F1(lx)
            FD = self.calculate_FD(l, s)
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
            h = val_data("Distancia desde el borde inferior del panel de chapa o el centro del área soportada por el refuerzo hasta la cubierta de cierre en la línea central (metros): ")
            pressure = self.N3 * h
            
        elif zone == 9: #Mamparos de Tanques Profundos
            ncgx = self.calculate_ncgx(lx)
            h = None
            pressure_1 = self.N3 * h
            pg = max(10.05, val_data("Peso especifico del liquido: "))
            h2 = val_data("Distancia desde el borde inferior del panel de chapa o el centro de la zona soportada por el refuerzo hasta la parte superior del depósito (metros): ")
            pressure_2 = pg * (1 + 0.5 * ncgx) * h2
            pressure = max(pressure_1, pressure_2)
            
        elif zone == 10: #Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos
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

            for location, (P1, P2) in pressures.items():
                if self.craft.L <= 12.2:
                    result[location] = P1
                elif self.craft.L > 30.5:
                    result[location] = P2
                else:
                    result[location] = np.interp(self.craft.L, [12.2, 30.5], [P1, P2])

            pressure = result
            
        elif zone == 11: #Túneles de Waterjets
            pressure = val_data("Presión máxima positiva o negativa de diseño del túnel [kN/m^2]: ", True, True, -1)
            
        else: #zone == 12 and 13
            pressure = 0
            
        return pressure

    def calculate_h13(self) -> float:
        h13_values = {1: 4, 2: 2.5, 3: 0.5}
        h13 = max(h13_values.get(self.craft.tipo_embarcacion), (self.craft.L / 12))
        return h13

    def calculate_ncgx(self, lx) -> tuple:
        kn = 0.256
        ncg_limit = 1.39 + kn * (self.craft.V / np.sqrt(self.craft.L))
        _ncg = self.N2 * (((12 * self.h13) / self.craft.BW) + 1) * self.craft.tau * (50 - self.craft.Bcg) * ((self.craft.V ** 2 * self.craft.BW ** 2) / self.craft.W)
        ncg = min(ncg_limit, _ncg)
        if self.craft.V > (18 * np.sqrt(self.craft.L)):
            ncg = 7 if self.craft.tipo_embarcacion == 4 else 6
        if self.craft.L < 24 and ncg < 1:
            ncg = 1

        #Calculo de nxx
        x_known = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        y_known = [0.8, 0.8, 0.8, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        Kv = np.interp(lx, x_known, y_known)
        ncgx = ncg * Kv
        
        return ncgx

    def calculate_FD(self, l, s) -> list:
        AR = 6.95 * self.craft.W / self.craft.d

        AD_plating = min(s * l, 2.5 * pow(s, 2))
        ADR_plating = AD_plating / AR

        AD_stiffening = max(s * l, 0.33 * pow(l, 2))
        ADR_stiffening = AD_stiffening / AR

        x_known = [0.001, 0.005, 0.010, 0.05, 0.100, 0.500, 1]
        y_known = [1, 0.86, 0.76, 0.47, 0.37, 0.235, 0.2]

        FD_plating = np.interp(ADR_plating, x_known, y_known)
        FD_plating = min(max(FD_plating, 0.4), 1.0)

        FD_stiffening = np.interp(ADR_stiffening, x_known, y_known)
        FD_stiffening = min(max(FD_stiffening, 0.4), 1.0)
        
        return FD_plating, FD_stiffening

    def calculate_FV(self, lx) -> float:
        x_known = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.445, 0.4, 0.3, 0.2, 0.1, 0]
        y_known = [0.25, 0.39, 0.52, 0.66, 0.8, 0.92, 1, 1, 1, 1, 1, 0.5]
        FV = np.interp(lx, x_known, y_known)
        FV = min(max(FV, 0.25), 1.0)
        return FV

    def calculate_F1(self, lx) -> float:
        x_known = [0, 0.2, 0.7, 0.8, 1.0]
        y_known = [0.5, 0.4, 0.4, 1.0, 1.0]
        F1 = np.interp(lx, x_known, y_known)
        return F1

    def decks_pressures(self): #Revisar función
        """ Las diferentes cubiertas posibles están enumeradas """
        cubiertas_proa = 0.20 * self.craft.L +7.6                                                   #1
        cubiertas_popa = 0.10 * self.craft.L + 6.1                                                  #2
        cubiertas_alojamientos = 5                                                                  #3     
        carga = val_data("Carga en la cubierta (kN/m^2): ", True, True, -1)                         
        cubiertas_carga = carga * (1 + 0.5 * self.nxx)                                              #4
        cargo_density = max(val_data("Densidad de la carga (kN/m^3): ", True, True, -1), 7.04)      
        height = val_data("Altura del almacén (metros): ", True, True, -1)
        almacenes_maquinaria_otros = cargo_density * height * (1 + 0.5 * self.nxx)                  #5


class Acero_Aluminio_Plating:  # Plating de: Acero Aluminio && Aluminum Extruded Planking and aluminum Corrugated Panels

    
    def __init__(self, craft: Craft, pressure: Pressures) -> None:
        self.craft = craft
        self.pressure = pressure
        
        
    def thickness(self):
        # Diccionario para almacenar los valores de espesor calculados
        thickness_values = {}
        
        # Iterar sobre las zonas seleccionadas en la instancia de Craft
        for zone in self.craft.selected_zones:
            if zone == 12:
                espesor = self.boat_thrusters_tunnels()
            else:
                # Obtener dimensiones l y s para la zona específica
                s = val_data(f"Separación entre refuerzos o lado más corto del panel en la zona: {self.craft.ZONES[zone]} (cm): ", True, True, -1)
                l = val_data(f"Longitud sin apoyo de los refuerzos o lado mayor del panel en la zona: {self.craft.ZONES[zone]} (cm): ", True, True, -1, s)
                
                #Esfuerzo de diseño de la zona
                sigma_a = self.design_stress(zone)
                pressure = self.pressure.calculate_pressures(zone, l, s)
                 
                # Calcular el espesor para la zona especificada
                if zone in [2, 3, 4, 5, 8, 9]:
                    espesor = max(self.lateral_loading(zone, l, s, pressure, sigma_a), self.secondary_stiffening(l, s), self.minimum_thickness(zone))
                elif zone in [6, 7, 10]:
                    espesor = max(self.lateral_loading(zone, l, s, pressure, sigma_a), self.secondary_stiffening(l, s))
                elif zone == 11:
                    espesor = self.lateral_loading(zone, l, s, pressure, sigma_a)
                else:  # zone == 13
                    espesor = self.operation_decks(l, s)
            
            # Almacenar el espesor calculado junto con el nombre de la zona en el diccionario thickness_values
            thickness_values[self.craft.ZONES[zone]] = espesor
            
            # Imprimir el espesor calculado
            print(f"Zona: {self.craft.ZONES[zone]}, Espesor: {espesor}")

        # Retornar el diccionario con los valores de espesor calculados
        return thickness_values
    
    def design_stress(self, zone) -> float:    #Corregir
        # Asegurarse que sigma_y no sea mayor que 0.7 * sigma u
        sigma = min(self.craft.sigma_y, 0.7 * self.craft.sigma_u)
        
        # Iterar sobre las zonas seleccionadas y calcular los esfuerzos de diseño
        if zone in [2, 3]:
            bottom_pressure, is_slamming = self.pressure.bottom_pressure()
            if is_slamming:
                d_stress = 0.90 * sigma
            else:
                d_stress = 0.55 * sigma
        elif zone in [4, 5, 7, 9, 10]:
            d_stress = 0.60 * sigma
        elif zone == 6:
            d_stress = 0.90 * sigma
        elif zone == 8:
            d_stress = 0.95 * sigma
        elif zone == 11:
            bottom_pressure, is_slamming = self.pressure.bottom_pressure()
            if is_slamming:
                d_stress = 0.60 * sigma
            else:
                d_stress = 0.55 * sigma
        else:
            d_stress = "No aplicable"
        
        return d_stress

    def lateral_loading(self, pressure, l, s, sigma_a) -> float: #Falta implemntar pressures, waterjets y k1
        ls_known = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        k_known = [0.308, 0.348, 0.383, 0.412, 0.436, 0.454, 0.468, 0.479, 0.487, 0.493, 0.500]
        k1_known = [0.014, 0.017, 0.019, 0.021, 0.024, 0.024, 0.025, 0.026, 0.027, 0.027, 0.028]

        ls = l / s

        if ls > 2.0:
            k = 0.500
            k1 = 0.028
        elif ls < 1.0:
            k = 0.308
            k1 = 0.014
        else:
            k = np.interp(ls, ls_known, k_known)
            k1 = np.interp(ls, ls_known, k1_known)
            
        p = self.pressure.water_jet_tunnels_pressure if zone == 11 else pressure
            
        lateral_loading = s * 10 * np.sqrt((pressure * k)/(1000 * sigma_a))
        return lateral_loading

    def secondary_stiffening(self, s) -> float:
        if self.craft.material == "Acero":
            return 0.01 * s
        else:
            return 0.012 * s

    def minimum_thickness(self, zone) -> float:
        if self.craft.material == 'Acero':
            q = 1.0 if self.craft.resistencia == "Alta" else 245 / self.craft.sigma_y
        else:
            q = 115 / self.craft.sigma_y
        
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

    def boat_thrusters_tunnels(self) -> float:    #Revisar
        #Transverse Thruster Tunnels/Tubes (Boat Thruster)
        t = 0.008 * d * np.sqrt(Q) + 3.0
        return t
    
    def operation_decks(self) -> float:    #Revisar
        #Decks Provided for the Operation or Stowage of Vehicles
        t = np.sqrt((beta * W *(1 + 0.5 * nxx)) / sigma_a)
        return t








class Aluminium_Sandwich_Panels:
    def __init__(self):
        pass
    # sm_skins = (np.pow(s, 2) * pressure * k) / (6e5 *d_stress)
    # I_skins = (np.pow(s, 3) * pressure * k1) / (120e5 * 0.24 * E)
    # core_shear = (v * p * s) / tau     #The thickness of core and sandwich is to be not less than given by the following equation:
    # #core_shear:=(do + dc) / 2     #do = thickness of overall sandwich, dc = thickness of core



    # #  Fiber Reinforced Plastic
    # sigma_a = 0.33 * sigma_u   # Design Stresses

    # def calculate_ks_kl(l, s, Es, El):
    #     # Calcular (l/s) * (Es / El)^0.25
    #     aspect_ratio = (l / s) * np.power((Es / El), 0.25)

    #     # Valores de la tabla
    #     aspect_ratios = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    #     ks_values = [0.308, 0.348, 0.383, 0.412, 0.436, 0.454, 0.468, 0.479, 0.487, 0.493, 0.497]
    #     kl_values = [0.308, 0.323, 0.333, 0.338, 0.342, 0.342, 0.342, 0.342, 0.342, 0.342, 0.342]

    #     # Determinar ks y kl basado en aspect_ratio
    #     if aspect_ratio > 2.0:
    #         ks = 0.500
    #         kl = 0.342
    #     elif aspect_ratio < 1.0:
    #         ks = 0.308
    #         kl = 0.308
    #     else:
    #         # Interpolación usando numpy
    #         ks = np.interp(aspect_ratio, aspect_ratios, ks_values)
    #         kl = np.interp(aspect_ratio, aspect_ratios, kl_values)

    #     return aspect_ratio, ks, kl

    # #   With Essentially Same Properties in 0° and 90° Axes
    # c = max((1-A/s), 0.70)
    # t = s * c * np.sqrt((pressure * k) / (1000 * d_stress)) #1

    # t = s * np.pow(c, 3) * np.sqrt((pressure * k1) / (1000 * k2 * E_F)) #2

    # #Strength deck and shell #L is generally not to be taken less than 12.2 m (40 ft).
    # t = k3 * (c1 + 0.26 * self.craft.L) * np.sqrt(q1) #3

    # #Strength deck and bottom shell
    # t = (s/kb) * np.sqrt((0.6 * sigma_uc) / E_c) * np.sqrt(SM_R / SM_A) #4


    # #With Different Properties in 0° and 90° Axes
    # t = s * c * np.sqrt((pressure * ks) / (1000 * d_stress))    #1
    # t = s * c * np.sqrt((pressure * kl) / (1000 * d_stress)) * np.pow((El / Es), 0.25)  #2
