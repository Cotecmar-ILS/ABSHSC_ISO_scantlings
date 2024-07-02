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
        self.LW = val_data("Eslora de flotación (metros): ", True, True, -1, 0, self.L)
        self.B = val_data("Manga Total (metros): ")
        self.BW = val_data("Manga de flotación (metros): ", True, True, -1, 0, self.B)
        self.D = val_data("Puntal (metros): ")
        self.d = val_data("Calado (metros): ", True, True, 0,0.04 * self.L, self.D)
        self.V = val_data("Velocidad maxima (nudos): ", True, True, -1, 0, 20 if self.L > 61 else None)
        self.W = val_data("Desplazamiento de la embarcación (kg): ")
        self.Bcg = val_data("Ángulo de astilla muerta fondo en LCG (°grados): ")
        self.tau = val_data("Ángulo de trimado a velocidad máxima (grados): ", True, True, -1, 3)
        self.tipo_embarcacion = self.select_tipo_embarcacion()
        self.material = self.select_material()
        # self.sigma_u = val_data("Esfuerzo ultimo a la tracción (MPa): ")
        # self.sigma_y = val_data("Limite elastico por tracción (MPa): ")
        self.resistencia = self.determine_resistencia()
        self.selected_zones = self.select_zones()
        
        
    def display_menu(self, items) -> None:
        #Funcion auxiliar para consola
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


class Plating:


    def __init__(self, craft: Craft, pressure: Pressures) -> None:
        self.craft = craft
        self.pressure = pressure
        self.context = "Plating"


    def thickness(self) -> dict:
        # Diccionario para almacenar los valores de espesor calculados
        thickness_values = {}

        # Iterar sobre las zonas seleccionadas en la instancia de Craft
        for zone in self.craft.selected_zones:
            if self.craft.material in ['Acero', 'Aluminio', 'Aluminio extruido']:
                if zone == 12:
                    espesor = self.boat_thrusters_tunnels()
                else:
                    #Obtener dimensiones l y s para la zona específica
                    #if self.craft.material == Acero or Aluminio:
                        # MOSTRAR IMAGEN 4
                    #elif self.craft.material == Extruded Planking:
                        # MOSTRAR IMAGEN 5
                    s = val_data(f"Separación entre refuerzos o lado más corto del panel en la zona: {self.craft.ZONES[zone]} (mm): ", True, True, -1)
                    l = val_data(f"Longitud sin apoyo de los refuerzos o lado mayor del panel en la zona: {self.craft.ZONES[zone]} (mm): ", True, True, -1, s)
                    sigma_u = val_data("Esfuerzo ultimo a la tracción (MPa): ")
                    sigma_y = val_data("Limite elastico por tracción (MPa): ")
                    
                    #Esfuerzo de diseño de la zona
                    pressure, index = self.pressure.calculate_pressures(self.context, zone, l, s)
                    sigma_a = self.design_stress(zone, index)
                    k = self.constant_k(l, s)
                    
                    # Calcular el espesor para la zona especificada
                    if zone in [2, 3, 4, 5, 8, 9]:
                        espesor = max(self.lateral_loading(zone, l, s, pressure, sigma_a, k), self.secondary_stiffening(s), self.minimum_thickness(zone))
                    elif zone in [6, 7]:
                        espesor = max(self.lateral_loading(zone, l, s, pressure, sigma_a, k), self.secondary_stiffening(s))
                    elif zone == 10:
                        espesor = self.superstructure(pressure, l, s, sigma_a)
                    elif zone == 11:
                        espesor = self.lateral_loading(zone, l, s, pressure, sigma_a, k)
                    elif zone == 13:  
                        espesor = self.operation_decks(l, s, zone, sigma_a)

                # Almacenar el espesor calculado junto con el nombre de la zona en el diccionario thickness_values
                thickness_values[self.craft.ZONES[zone]] = espesor

                # Imprimir el espesor calculado
                if zone != 10:
                    print(f"Zona: {self.craft.ZONES[zone]}, Espesor: {espesor}")
            
            elif self.craft.material == 'Aluminio en Sandwich':
                # Obtener las dimensiones de la zona
                l = val_data(f"Longitud sin apoyo de los refuerzos o lado mayor del panel en la zona: {self.craft.ZONES[zone]} (mm): ", True, True, -1)
                s = val_data(f"Separación entre refuerzos o lado más corto del panel en la zona: {self.craft.ZONES[zone]} (mm): ", True, True, -1)
                k = self.constant_k(l, s)
                k1 = self.constant_k1(l, s)
                al_sm_skins = self.aluminum_sandwich_section_modulus_skins(pressure, s, sigma_a, k)
                al_inertia_skins = self.aluminum_sandwich_inertia_skins(pressure, s, sigma_a, k1)
                al_core = self.aluminum_sandwich_core_shear(pressure, s, sigma_a, k)
                
                print(f"Zona: {self.craft.ZONES[zone]}, Modulo de seccion del laminado: {al_sm_skins} [cm^3], Inercia del laminado: {al_inertia_skins} [cm^4], Resistencia al cortante del nucleo: {al_core} [MPa]")

            elif self.craft.material == 'Fibra laminada':
                tipo_laminado = val_data("Utiliza diferentes tipos de fibra? (1): No (2): Si: ", False, True, -1, 1, 2)
                if tipo_laminado == 1:
                    if zone in [2, 4]:
                        espesor = max(self.laminated_same_properties(pressure, s, d_stress, k), self.laminated_second_equation, self.laminated_third_equation(zone, pressure, s, d_stress), self.laminated_fourth_equation(zone, pressure, s, d_stress))
                    elif zone == 3:
                        espesor = max(self.laminated_same_properties(pressure, s, d_stress, k), self.laminated_second_equation, self.laminated_third_equation(zone, pressure, s, d_stress))
                    else:
                        espesor = max(self.laminated_same_properties(pressure, s, d_stress, k), self.laminated_second_equation(zone, pressure, s, d_stress))
                else: # tipo_laminado == 2
                    espesor = max(self.laminated_fifth_equation(zone, pressure, s, d_stress, kl, ks, El), self.laminated_sixth_equation(zone, pressure, s, d_stress, kl, ks, El, Es))    
                print(f"Zona: {self.craft.ZONES[zone]}, Espesor: {espesor} mm")
            
            elif self.craft.material == 'Fibra en Sandwich':
                espesor = max(self.sandwich_same_properties_innerskin(pressure, s, d_stress, k), self.sandwich_same_properties_outerskin(pressure, s, d_stress, k))
                print(f"Zona: {self.craft.ZONES[zone]}, Espesor: {espesor} mm")

        # Retornar el diccionario con los valores de espesor calculados
        return thickness_values

    def design_stress(self, zone, sigma_y, sigma_u, index) -> float:
        # Asegurarse que sigma_y no sea mayor que 0.7 * sigma u
        sigma = min(sigma_y, 0.7 * sigma_u)

        if zone in [2, 3]:
            if index == True:
                d_stress = 0.90 * sigma
            else:
                d_stress = 0.55 * sigma
        elif zone in [4, 5, 7, 9, 10, 13]:
            d_stress = 0.60 * sigma
        elif zone == 6:
            d_stress = 0.90 * sigma
        elif zone == 8:
            d_stress = 0.95 * sigma
        elif zone == 11:
            if index == True:
                d_stress = 0.60 * sigma
            else:
                d_stress = 0.55 * sigma
        else:
            d_stress = "No aplicable"
        
        return d_stress

    def constant_k(self, l, s) -> float:
        ls_known = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        k_known = [0.308, 0.348, 0.383, 0.412, 0.436, 0.454, 0.468, 0.479, 0.487, 0.493, 0.500]
        ls = l / s
        if ls > 2.0:
            k = 0.500
        elif ls < 1.0:
            k = 0.308
        else:
            k = np.interp(ls, ls_known, k_known)
        return k
    
    def constant_k1(self, l, s) -> float:
        ls_known = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        k1_known = [0.014, 0.017, 0.019, 0.021, 0.024, 0.024, 0.025, 0.026, 0.027, 0.027, 0.028]
        ls = l / s
        if ls > 2.0:
            k1 = 0.028
        elif ls < 1.0:
            k1 = 0.014
        else:
            k1 = np.interp(ls, ls_known, k1_known)
        return k1

    def superstructure(self, pressures, l, s, sigma_a) -> dict:
        """
        Calcula el espesor necesario para cada parte de la zona 10 basada en las presiones proporcionadas.

        Parámetros:
            pressures (dict): Diccionario con las presiones para cada ubicación específica.
            l (float): Longitud sin apoyo de los refuerzos o lado mayor del panel en mm.
            s (float): Separación entre refuerzos o lado más corto del panel en mm.
            sigma_a (float): Tensión de diseño.

        Retorna:
            dict: Diccionario con los espesores calculados para cada ubicación.
        """
        thickness_values = {}
        secondary_stiffening = self.secondary_stiffening(s)

        for location, pressure_value in pressures.items():
            thickness = max(self.lateral_loading(10, pressure_value, l, s, sigma_a), secondary_stiffening)
            thickness_values[location] = thickness
            print(f"Ubicación: {location}, Espesor: {thickness}")

        return thickness_values

    def boat_thrusters_tunnels(self) -> float:
        #Transverse Thruster Tunnels/Tubes (Boat Thruster)
        if self.craft.L > 40:
            d = val_data("Diametro interno del tunel (mm): ", True, True, -1, 968)
        else: #self.craft.L <= 40:
            d = val_data("Diametro interno del tunel (mm): ", True, True, -1, 600)
        Q = self.calculate_Q()
        t = 0.008 * d * np.sqrt(Q) + 3.0
        return t
    
    def operation_decks(self, l, s, zone, sigma_a) -> float:
        # Decks Provided for the Operation or Stowage of Vehicles
        x, y, Bx = self.pressure.calculate_x_y_Bx(zone)
        ncgx = self.pressure.calculate_ncgx(x)
        # Mostrar imagen 5
        W = val_data("Carga estática de la rueda (N): ")
        a = val_data("Ingrese la dimensión de la huella de la rueda paralela al borde más corto, a (mm): ", True, True)
        b = val_data("Ingrese la dimensión de la huella de la rueda paralela al borde más largo, b (mm): ", True, True)
        
        # Calcular beta
        beta = self.calculate_beta(a, b, s, l)
        
        # Calcular el espesor t
        t = np.sqrt((beta * W * (1 + 0.5 * ncgx)) / sigma_a)
        
        return t

    def calculate_Q(self, sigma_y, sigma_u) -> float:
        if self.craft.material == "Acero":
            yield_point = {
                "Acero de resistencia ordinaria": (206.842, 234.421),
                "Acero de grado H32": (234.421, 313.711),
                "Acero de grado H36": (313.711, 351.632)
            }
            tensile_strength = {
                "Acero de resistencia ordinaria": (399.895, 517.106),
                "Acero de grado H32": (441.264, 586.054),
                "Acero de grado H36": (489.527, 620.528)
            }
            grado_acero = "Otros Aceros"  # Valor por defecto
            for grado in yield_point:
                min_yield, max_yield = yield_point[grado]
                min_tensile, max_tensile = tensile_strength[grado]
                if (min_yield <= sigma_y <= max_yield) and (min_tensile <= sigma_u <= max_tensile):
                    grado_acero = grado
                    break
            # Asignación de coeficiente Q dependiendo del grado de acero:
            if grado_acero == "Acero de resistencia ordinaria":
                return 1.0
            elif grado_acero == "Acero de grado H32":
                return 0.78
            elif grado_acero == "Acero de grado H36":
                return 0.72
            else:  # "Otros Aceros"
                return 490 / (min(sigma_y, 0.7 * sigma_u) + 0.66 * sigma_u)

        elif self.craft.material == "Aluminio":
            sigma = min(sigma_y, 0.7 * sigma_u)
            q5 = 115 / sigma
            Qo = 635 / (sigma + sigma_u)
            return max(0.9 + q5, Qo)

        elif self.craft.material in ('Fibra laminada', 'Fibra en sandwich'):
            return 400 / (0.75 * sigma_u)
        else:
            raise ValueError(
                f"El material {self.craft.material}, no se encuentra en la base de datos")

    def calculate_beta(self, a, b, s, l) -> float:
        # Definimos las tablas de valores de Beta
        beta_values = {
            1: np.array([
                [0, 1.82, 1.38, 1.12, 0.93, 0.76],
                [1.82, 1.28, 1.08, 0.90, 0.63, 0.63],
                [1.39, 1.07, 0.84, 0.72, 0.52, 0.52],
                [1.12, 0.90, 0.74, 0.60, 0.43, 0.42],
                [0.92, 0.76, 0.62, 0.51, 0.42, 0.36],
                [0.76, 0.63, 0.52, 0.42, 0.35, 0.30]
            ]),
            1.4: np.array([
                [0, 2.00, 1.55, 1.20, 0.84, 0.75],
                [1.78, 1.43, 1.23, 0.95, 0.74, 0.63],
                [1.39, 1.13, 1.00, 0.80, 0.62, 0.55],
                [1.12, 0.92, 0.82, 0.68, 0.53, 0.47],
                [0.90, 0.76, 0.68, 0.57, 0.45, 0.38],
                [0.75, 0.62, 0.57, 0.47, 0.38, 0.30]
            ]),
            2: np.array([
                [0, 1.64, 1.20, 0.97, 0.78, 0.64],
                [1.73, 1.31, 1.03, 0.80, 0.68, 0.57],
                [1.32, 1.08, 0.88, 0.76, 0.64, 0.50],
                [1.09, 0.90, 0.76, 0.70, 0.64, 0.44],
                [0.87, 0.76, 0.68, 0.64, 0.60, 0.44],
                [0.71, 0.61, 0.63, 0.55, 0.45, 0.38]
            ])
        }

        # Índices predefinidos para las filas y columnas según la tabla
        a_s_indices = np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        b_s_indices = {
            1: np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0]),
            1.4: np.array([0, 0.2, 0.4, 0.8, 1.2, 1.4]),
            2: np.array([0, 0.4, 0.8, 1.2, 1.6, 2.0])
        }

        # Calculamos las relaciones
        l_s = l / s
        a_s = a / s
        b_s = b / s

        # Selección de la tabla adecuada
        if l_s >= 2:
            tabla = beta_values[2]
            b_s_idx_array = b_s_indices[2]
        elif np.abs(l_s - 1.4) < np.abs(l_s - 1):
            tabla = beta_values[1.4]
            b_s_idx_array = b_s_indices[1.4]
        else:
            tabla = beta_values[1]
            b_s_idx_array = b_s_indices[1]

        # Encontrar el índice más cercano para a/s y b/s
        a_s_idx = np.abs(a_s_indices - a_s).argmin()
        b_s_idx = np.abs(b_s_idx_array - b_s).argmin()

        # Devolver el valor de Beta correspondiente
        beta = tabla[a_s_idx, b_s_idx]
        return beta


#Acero, Aluminio y Aluminio extruido

    def lateral_loading(self, zone, pressure, l, s, sigma_a, k) -> float:            
        lateral_loading = s * 10 * np.sqrt((pressure * k)/(1000 * sigma_a))
        return lateral_loading

    def secondary_stiffening(self, s) -> float:
        if self.craft.material == "Acero":
            return 0.01 * s
        else:
            return 0.012 * s

    def minimum_thickness(self, zone, sigma_y) -> float:
        if self.craft.material == 'Acero':
            q = 1.0 if self.craft.resistencia == "Alta" else 245 / sigma_y
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


#Aluminio en Sandwich

    def aluminum_sandwich_section_modulus_skins(self, pressure, s, k, sigma_a) -> float:
        sm_skins = (np.pow(s, 2) * pressure * k) / (6e5 * sigma_a)
        return sm_skins
    
    def aluminum_sandwich_inertia_skins(self, pressure, s, k1, E) -> float:
        I_skins = (np.pow(s, 3) * pressure * k1) / (120e5 * 0.24 * E)
        return I_skins
    
    def aluminum_sandwich_core_shear(self, pressure, s, v, tau) -> float:
        #core_shear:=(do + dc) / 2     #do = thickness of skins, dc = thickness of core
        core_shear = (v * pressure * s) / tau     #The thickness of core and sandwich is to be not less than given by the following equation
        return core_shear
    

#Fibra laminada

    def design_stress_fiber(self, sigma_u) -> float:
        #  Fiber Reinforced Plastic
        sigma_a = 0.33 * sigma_u   # Design Stresses
        return sigma_a
    
    def laminated_same_properties(self, pressure, s, d_stress, k) -> float:
        A = val_data("Medida perpendicularmente desde el espaciado entre refuerzos, s, hasta el punto más alto del arco de la placa curvada entre los bordes del panel: ")
        #   With Essentially Same Properties in 0° and 90° Axes
        c = max((1 - A/s), 0.70)
        espesor_a = s * c * np.sqrt((pressure * k) / (1000 * d_stress)) #1
        return espesor_a
    
    def laminated_second_equation(self, zone, pressure, s, d_stress) -> float:    
        if zone == 2:
            if self.craft.tipo_embarcacion == 4:
                k2 = 0.010
            else:
                k2 = 0.015
        elif zone == 3:
            if self.craft.tipo_embarcacion == 4:
                k2 = 0.015
            else:
                k2 = 0.020
        elif zone == 10:
            k2 = 0.025
        else:
            k2 = 0.010
        
        espesor_b = s * np.pow(c, 3) * np.sqrt((pressure * k1) / (1000 * k2 * E_F)) #2
        return espesor_b
    
    def laminated_third_equation(self, zone, pressure, s, d_stress, k3, sigma_uc, E_c, SM_R, SM_A, El, Es) -> float:    
        #Strength deck and shell #L is generally not to be taken less than 12.2 m (40 ft).
        espesor_c = k3 * (c1 + 0.26 * self.craft.L) * np.sqrt(q1) #3
        return espesor_c

    def laminated_fourth_equation(self, zone, pressure, s, d_stress, sigma_uc, E_c, SM_R, SM_A, El, Es, kb) -> float:
        #Strength deck and bottom shell
        espesor_d = (s/kb) * np.sqrt((0.6 * sigma_uc) / E_c) * np.sqrt(SM_R / SM_A) #4
        return espesor_d

    #With Different Properties in 0° and 90° Axes
    
    def laminated_fifth_equation(self, zone, pressure, s, d_stress, kl, ks, El, Es) -> float:
        t = s * c * np.sqrt((pressure * ks) / (1000 * d_stress))    #1
        return t
    
    def laminated_sixth_equation(self, zone, pressure, s, d_stress, kl, ks, El, Es) -> float:
        t = s * c * np.sqrt((pressure * kl) / (1000 * d_stress)) * np.pow((El / Es), 0.25)  #2
        return t


#Fibra en sandwich

    def sandwich_same_properties_outerskin(self, pressure, s, d_stress, k) -> float:
        A = val_data("Medida perpendicularmente desde el espaciado entre refuerzos, s, hasta el punto más alto del arco de la placa curvada entre los bordes del panel: ")
        #   With Essentially Same Properties in 0° and 90° Axes
        c = max((1 - A/s), 0.70)
        SM_o = (((s * c) ** 2) * pressure * k) / (6e10 * d_stress) 
        return SM_o
    
    

    
    
    
    
    #INTERNALS
    # def calculate_internals_SM(self) -> tuple:
    #     SM_values = []
    #     for i in range(len(self.d_stressi)):
    #         SM = (83.3*self.bottom_p*(self.s/100)*pow((self.l/100),2))/(self.d_stressi[i])
    #         SM_values.append(SM)
    #     return tuple(SM_values)
    
    # def calculate_K4(self) -> float:
    #     if self.material == 'Acero':
    #         if self.zone == "Bottom" or self.zone == "Side":
    #             return 0.0015
    #         else:
    #             return 0.0011
    #     elif self.material == "Aluminio":
    #         if self.zone == "Bottom" or self.zone == "Side":
    #             return 0.0021
    #         else:
    #             return 0.0018

    # def calculate_E(self) -> float:
    #     if self.material == 'Acero':
    #         return 2.06e5
    #     elif self.material == 'Aluminio':
    #         return 6.9e4

    # def moment_inertia(self) -> float:
    #     I = (260*self.bottom_p*(self.s/100)*pow((self.l/100),3))/ (self.K4*self.E)
    #     return I


def main():
    #Crear una instancia de la clase
    craft = Craft()
    pressures = Pressures(craft)
    plating = Acero_Aluminio_Plating(craft, pressures)
    plating.thickness()

if __name__ == "__main__":
    main()