"""
                ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS
--------------------------------------------------------------------------
MATERIALS = ('Steel', 'Aluminum', 'Aluminum Extruded Planking', 'Aluminum Sandwich Panels', 'Aluminum Corrugated', 'Single Skin Laminate Fiber Plastic', 'Sandwich Laminate Fiber Plastic') 
ZONES
    # Shell:
        #1 Hull Girder
        #2 Bottom Shell
        #3 Side Shell
        #4 Transom Shell
    # Decks:
        #5 Strength Deck
        #6 Lower Decks/Other Decks
        #7 Wet Decks
        #8 Superstructure and deckhouses Decks 
    # Bulkheads:
        #9 Water Tight Bulkheads
        #10 Deep Tank Bulkheads
    # Others:
        #11 Superstructure and Deckhouses - Front, Sides, Ends, and Tops
        #12 Water Jet Tunnels
        #13 Transverse Thruster Tunnels/Tubes (Boat Thruster)
        #14 Decks Provided for the Operation or Stowage of Vehicles
--------------------------------------------------------------------------
MATERIALS = ('Acero', 'Aluminio', 'Aluminio extruido', 'Aluminio Corrugado', 'Aluminio en Sandwich', 'Fibra laminada', 'Fibra en sandwich') 
ZONAS
    Casco:
        1. Vagra Maestra
        2. Casco de Fondo
        3. Casco de Costado
        4. Espejo de Popa
    Cubiertas:
        5. Cubierta Principal
        6. Cubiertas Inferiores/Otras Cubiertas
        7. Cubiertas Humedas
        8. Cubiertas de Superestructura y Casetas de Cubierta
    Mamparos:
        9. Mamparos Estancos
        10. Mamparos de Tanques Profundos
    Otros:
        11. Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos
        12. Túneles de Waterjets
        13. Túneles de Bow Thrusters
        14. Cubiertas de Operación o Almacenamiento de Vehículos
        
--------------------------------------------------------------------------
"""

import numpy as np
from validations import val_data


class Craft:
    
    
    def __init__(self):
        self.designer_name = input("Diseñador: ")
        self.boat_name = input("Embarcación: ")
        self.company_name = input("Empresa: ")
        self.management_name = input("Gerencia: ")
        self.division_name = input("División: ")
        self.values = {}
        self.material = self.get_material()
        self.selected_zones = self.get_zones()
        

    #Metodo para pedir datos y validar si ya existe
    def get_value(self, key, prompt, *args) -> float:
        if key not in self.values:
            self.values[key] = val_data(prompt, *args)
        return self.values[key]

    #Metodo para mostrar info solo para consola
    def display_menu(self, items) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def get_tipo_embarcacion(self) -> int:
        if 'tipo_embarcacion' not in self.values:
            print("\nSeleccione el tipo de embarcación")
            tipo_embarcacion = ('Alta velocidad', 'Costera', 'Fluvial', 'Búsqueda y rescate')
            self.display_menu(tipo_embarcacion)
            choice = val_data("Ingrese el número correspondiente: ", False, True, -1, 1, len(tipo_embarcacion))
            self.values['tipo_embarcacion'] = choice
        return self.values['tipo_embarcacion']
    
    def get_material(self) -> int:
        if 'material' not in self.values:
            print("\nLista de materiales disponibles")
            materiales = ('Acero', 'Aluminio', 'Aluminio extruido', 'Aluminio en Sandwich', 'Aluminio Corrugado', 'Fibra laminada', 'Fibra en sandwich')
            self.display_menu(materiales)
            choice = val_data("Ingrese el número correspondiente -> ", False, True, -1, 1, len(materiales))
            self.values['material'] = choice
        return self.values['material']
    
    def get_zones(self) -> list:
        if 'selected_zones' not in self.values:
            zonas = {
                1: 'Vagra Maestra',
                2: 'Casco de Fondo',
                3: 'Casco de Costado',
                4: 'Espejo de Popa',
                5: 'Cubierta de Principal',
                6: 'Cubiertas Inferiores/Otras Cubiertas',
                7: 'Cubiertas Humedas',
                8: 'Cubiertas de Superestructura y Casetas de Cubierta',
                9: 'Mamparos Estancos',
                10: 'Mamparos de Tanques Profundos',
                11: 'Superestructura y Casetas de Cubierta - Frente, Lados, Extremos y Techos',
                12: 'Túneles de Waterjets',
                13: 'Túneles de Bow Thrusters',
                14: 'Cubiertas de Operación o Almacenamiento de Vehículos'
            }

            available_zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] if self.material not in [1, 2] else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            print("\nSeleccione las zonas que desea escantillonar (ingrese '0' para finalizar)\n")
        
            # Mostrar las zonas disponibles desde una lista
            for number in available_zones:
                print(f"{number}. {zonas[number]}")
            selected_zones = []
            while True:
                try:
                    choice = int(input("\nIngrese el número correspondiente y presione Enter: "))
                    if choice == 0:
                        if not selected_zones:
                            raise ValueError("Debe seleccionar al menos una zona antes de finalizar.")
                        break
                    elif choice in available_zones:
                        if choice in selected_zones:
                            raise ValueError("Zona ya seleccionada, elija otra.")
                        selected_zones.append(choice)
                        print(f"Añadida: {zonas[choice]}")
                    else:
                        print("Selección no válida, intente de nuevo.")
                except ValueError as e:
                    print(e)
            self.values['selected_zones'] = selected_zones
        return self.values['selected_zones']
    
    def get_L(self) -> float:
        return self.get_value('L', "Eslora del casco (metros): ")

    def get_LW(self) -> float:
        L = self.get_L()  # Asegura que L es obtenido y validado primero
        return self.get_value('LW', "Eslora de flotación (metros): ", True, True, -1, 0, L)

    def get_B(self) -> float:
        return self.get_value('B', "Manga Total (metros): ")

    def get_BW(self) -> float:
        B = self.get_B()  # Asegura que B es obtenido y validado primero
        return self.get_value('BW', "Manga de flotación (metros): ", True, True, -1, 0, B)

    def get_D(self) -> float:
        return self.get_value('D', "Puntal (metros): ")

    def get_d(self) -> float:
        L = self.get_L()
        D = self.get_D()
        return self.get_value('d', "Calado (metros): ", True, True, 0, 0.04 * L, D)

    def get_V(self) -> float:
        L = self.get_L()
        return self.get_value('V', "Velocidad maxima (nudos): ", True, True, -1, 0, 20 if L > 61 else None)

    def get_W(self) -> float:
        return self.get_value('W', "Desplazamiento de la embarcación (kg): ")

    def get_Bcg(self) -> float:
        return self.get_value('Bcg', "Ángulo de astilla muerta fondo en LCG (°grados): ")

    def get_tau(self) -> float:
        return self.get_value('tau', "Ángulo de trimado a velocidad máxima (grados): ", True, True, -1, 3)
    
    def get_h13(self) -> float:
        L = self.get_L()
        tipo_embarcacion = self.get_tipo_embarcacion()
        h13_values = {1: 4, 2: 2.5, 3: 0.5, 4: 4}
        h13 = max(h13_values.get(tipo_embarcacion), (L / 12))
        return h13
    
    def get_sigma_y(self) -> float:
        return self.get_value('sigma_y', "Esfuerzo último a la tracción (MPa): ")
    
    def get_sigma_u(self) -> float:
        return self.get_value('sigma_u', "Límite elástico por tracción (MPa): ")
    
    def get_sigma_uf(self) -> float:
        return self.get_value('sigma_uf', "Resistencia mínima a la flexión (MPa): ")
    
    def get_sigma_uo(self) -> float:
        return self.get_value('sigma_uo', "Resistencia a la tracción de la fibra externa (MPa): ")
    
    def get_sigma_ui(self) -> float:
        return self.get_value('sigma_ui', "Resistencia a la tracción de la fibra interna (MPa): ")
    
    def get_sigma_ub(self) -> float:
        return self.get_value('sigma_ub', "Menor de las resistencias a la tracción o a la compresión (MPa): ")
    
    def get_l(self, zone, s) -> float:
        return val_data(f"Longitud mas larga de los paneles de {zone} (mm): ", True, True, 0, s)
    
    def get_s(self, zone, l) -> float:
        return val_data(f"Longitud mas corta de los paneles de {zone} (mm): ")
    

class ZonePressures:

    def __init__(self, craft):
        self.craft = craft
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        self.pressure_results = {}

    # Función principal para calculo de presiones (Controlador)
    def calculate_pressure(self, zone, context):
        if zone in [2, 3, 7, 8, 9]:
            s = val_data(f"Longitud mas corta de los paneles (mm): ")
            l = val_data(f"Longitud mas larga de los paneles (mm): ", True, True, 0, s)
        if zone == 2:
            pressure, index = self.casco_fondo(zone, context, s, l)
            self.pressure_results[zone] = pressure
            return pressure, index, s, l
        elif zone == 3:
            pressure, index = self.casco_costado(zone, context, s, l)
            self.pressure_results[zone] = pressure
            return pressure, index, s, l
        elif zone == 4:
            pressure, index = self.espejo_popa(context)
            self.pressure_results[zone] = pressure
            return pressure
        elif zone == 5:
            pressure, index = self.cubierta_principal()
            self.pressure_results[zone] = pressure
            return pressure
        elif zone == 6:
            pressure, index = self.cubiertas_inferiores_otras()
            self.pressure_results[zone] = pressure
            return pressure
        elif zone == 7:
            pressure, index = self.cubiertas_humedas(zone, context, s, l)
            self.pressure_results[zone] = pressure
            return pressure, s, l
        elif zone == 8:
            pressure, index = self.cubiertas_superestructura_casetas(zone, context, s, l)
            self.pressure_results[zone] = pressure
            return pressure, s, l
        elif zone == 9:
            pressure, index = self.mamparos_estancos(zone, context, s, l)
            self.pressure_results[zone] = pressure
            return pressure, s, l
        elif zone == 10:
            pressure, index = self.mamparos_tanques_profundos(zone)
            self.pressure_results[zone] = pressure
            return pressure
        elif zone == 11:
            pressure, index = self.superestructura_casetas(context)
            self.pressure_results[zone] = pressure
            return pressure
        elif zone == 12:
            pressure, index = self.tuneles_waterjets()
            self.pressure_results[zone] = pressure
            return pressure
        else:
            pressure = None
            return pressure

    # Funciones por zona
    def casco_fondo(self, zone, context, s, l):
        L = self.craft.get_L()
        LW = self.craft.get_LW()
        BW = self.craft.get_BW()
        d = self.craft.get_d()
        W = self.craft.get_W()
        Bcg = self.craft.get_Bcg()
        
        x, y, Bx = self.calculate_x_y_Bx(zone)
        ncgx = self.calculate_ncgx(x)
        FD = self.calculate_FD(context, l, s)
        FV = self.calculate_FV(x)
        H = self.calculate_H()
        
        if L >= 61:
            if x is None:
                slamming_pressure = ((self.N1 * W) / (LW * BW)) * (1 + ncgx) * FD
            else:  # x is not None
                slamming_pressure = ((self.N1 * W) / (LW * BW)) * (1 + ncgx) * ((70 - Bx) / (70 - Bcg)) * FD
        else:  # self.craft.L < 61
            slamming_pressure = ((self.N1 * W) / (LW * BW)) * (1 + ncgx) * FD * FV

        hidrostatic_pressure = self.N3 * (0.64 * H + d)

        index = "slamming pressure" if slamming_pressure > hidrostatic_pressure else "hidrostatic pressure"
        pressure = max(slamming_pressure, hidrostatic_pressure)
        
        return pressure, index

    def casco_costado(self, zone, context, s, l):
        L = self.craft.get_L()
        LW = self.craft.get_LW()
        BW = self.craft.get_BW()
        W = self.craft.get_W()
        Bcg = self.craft.get_Bcg()
        
        x, y, Bx = self.calculate_x_y_Bx(zone)
        ncgx = self.calculate_ncgx(x)
        FD = self.calculate_FD(context, l, s)
        Hs = self.calculate_Hs()
        
        if x is None:
            slamming_pressure = ((self.N1 * W) / (LW * BW)) * (1 + ncgx) * FD
            hidrostatic_pressure = self.N3 * Hs
        else:
            slamming_pressure = ((self.N1 * W) / (LW * BW)) * (1 + ncgx) * ((70 - Bx) / (70 - Bcg)) * FD
            hidrostatic_pressure = self.N3 * (Hs - y)
            
        index = slamming_pressure > hidrostatic_pressure    
        pressure = max(slamming_pressure, hidrostatic_pressure)
        
        return pressure, index

    def espejo_popa(self, context):
        if self.pressure_results[3] is None:
            print("\nPrimero se debe calcular la presión del costado\n")
            _s = val_data(f"Longitud mas corta de los paneles del costado (mm): ")
            _l = val_data(f"Longitud mas larga de los paneles del costado (mm): ", True, True, 0, _s)
            pressure_costado, index = self.casco_costado(3, context, _s, _l)
            self.pressure_results[3] = pressure_costado, index
        else:
            pressure_costado, index = self.pressure_results[3]
        
        L = self.craft.get_L()
        V = self.craft.get_V()
        
        Fa = 3.25 if context == 'Plating' else 1
        Cf = 0.0125 if L < 80 else 1.0
        # MOSTRAR IMAGEN 1
        alfa = val_data("Ángulo de ensanchamiento (grados): ")
        beta = val_data("Ángulo de entrada (grados): ")
        pressure_forend = 0.28 * Fa * Cf * self.N3 * (0.22 + 0.15 * np.tan(alfa)) * ((0.4 * V * np.cos(beta) + 0.6 * L ** 0.5) ** 2)
        
        pressure = max(pressure_costado, pressure_forend)

        return pressure, index
        
    def cubierta_principal(self):
        L = self.craft.get_L()
        pressure = 0.20 * L + 7.6
        return pressure
    
    def cubiertas_inferiores_otras(self):
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
        L = self.craft.get_L()
        pressure = 0.10 * L + 6.1
        return pressure

    def cubiertas_humedas(self, zone, context, s, l):
        L = self.craft.get_L()
        D = self.craft.get_D()
        d = self.craft.get_d()
        V = self.craft.get_V()
        h13 = self.get_h13()
        
        x, y, Bx = self.calculate_x_y_Bx(zone)
        F1 = self.calculate_F1(x)
        FD = self.calculate_FD(context, l, s)
        
        # Mostrar imagen 2
        ha = val_data("Altura desde la línea de flotación hasta la cubierta humeda en cuestión (metros): ", True, True, 0, 0, D - d)
        if L < 61:
            v1 = ((4 * h13) / (np.sqrt(L))) + 1
            pressure = 30 * self.N1 * FD * F1 * V * v1 * (1 - 0.85 * ha / h13)
        else:
            v1 = 5 * np.sqrt(h13 / L) + 1
            pressure = 55 * FD * F1 * np.pow(V, 0.1) * v1 * (1 - 0.35 * (ha / h13))
            
        return pressure

    def cubiertas_superestructura_casetas(self):
        L = self.craft.get_L()
        pressure = 0.10 * L + 6.1
        return pressure

    def mamparos_estancos(self):
        #Mostrar Imagen 3 - ISO 12215-5
        h = val_data("Altura del mamparo (metros): ")
        pressure = self.N3 * h
        return pressure

    def mamparos_tanques_profundos(self, zone): #Insertar imagen
        x, y, Bx = self.calculate_x_y_Bx(zone)
        ncgx = self.calculate_ncgx(x)

        #Mostrar Imagen 3 - ISO 12215-5
        hb = val_data("Altura de la columna de agua (metros): ") 
        pg = max(10.05, val_data("Peso especifico del liquido (kN/m^3): ", True, True, -1, 0, 10.05))
        pressure_1 = self.N3 * hb
        pressure_2 = pg * (1 + 0.5 * ncgx) * hb
        pressure = max(pressure_1, pressure_2)
        return pressure

    def superestructura_casetas(self, context):
        """
        A superstructure is an enclosed structure above the freeboard deck having side plating as an extension of
        the shell plating, or not fitted inboard of the hull side more than 4% of the breadth B.

        Una superestructura es una estructura cerrada situada por encima de la cubierta de francobordo que tiene 
        una chapa lateral como prolongación de la chapa del forro exterior, o que no está instalada en el interior 
        del costado del casco más del 4% de la manga.
        """
        L = self.craft.get_L()
        
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
            if L <= 12.2:
                result[location] = P1
            elif L > 30.5:
                result[location] = P2
            else:
                result[location] = np.interp(L, [12.2, 30.5], [P1, P2])
                
        #Retorna un diccionario
        pressure = result

        return pressure

    def tuneles_waterjets(self, context):
        if self.pressure_results[2] is None:
            print("\nPrimero se debe calcular la presión del fondo\n")
            _s = val_data(f"Longitud mas corta de los paneles del fondo (mm): ")
            _l = val_data(f"Longitud mas larga de los paneles del fondo (mm): ", True, True, 0, _s)
            pressure_fondo, index = self.casco_fondo(2, context, _s, _l)
            self.pressure_results[2] = pressure_fondo
        else:
            pressure_fondo, index = self.pressure_results[2]
        pressure = val_data("Presión máxima positiva o negativa de diseño del túnel [kN/m^2]: ", True, True, -1)
        return pressure, index

    # Funciones auxiliares
    def calculate_x_y_Bx(self, zone) -> tuple: #Corregir
        ask = val_data(f"¿Desea realizar el análisis en algún punto específico de la zona: {zone}, 0 = No, 1 = Si ?\n", False, False, 0, 0, 1)
        
        if ask == 1:
            x = val_data("Distancia desde proa hasta el punto de análisis (metros): ", True, True, -1, 0, self.craft.get_L())
            x = x / self.craft.get_L()
            Bx = val_data("Ángulo de astilla muerta de costado en el punto de análisis (grados): ", True, True, -1, 0, 55)
            
            if zone == 2:
                return x, None, Bx
            elif zone == 3:
                y = val_data("Altura sobre la linea base hasta el punto de análisis (metros): ", True, True, 0, 0, self.craft.get_D())
                return x, y, Bx

        return None, None, None  # Si el usuario no desea análisis específico o la zona no requiere análisis específico
    
    def calculate_ncgx(self, x) -> float:
        kn = 0.256
        ncgx_limit = 1.39 + kn * (self.craft.get_V() / np.sqrt(self.craft.get_L()))
        _ncgx = self.N2 * (((12 * self.craft.get_h13()) / self.craft.get_BW()) + 1) * self.craft.get_tau() * (50 - self.craft.get_Bcg()) * ((self.craft.get_V() ** 2 * self.craft.get_BW() ** 2) / self.craft.get_W())
        ncgx = min(ncgx_limit, _ncgx)
        if self.craft.get_V() > (18 * np.sqrt(self.craft.get_L())):
            ncgx = 7 if self.craft.get_tipo_embarcacion() == 4 else 6
        if self.craft.get_L() < 24 and ncgx < 1:
            ncgx = 1

        # Ajuste de ncgx basado en x
        if x is not None:
            x_known = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            y_known = [0.8, 0.8, 0.8, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
            Kv = np.interp(x, x_known, y_known)
            ncgx = ncgx * Kv

        return ncgx

    def calculate_FD(self, context, s, l) -> float:
        AR = 6.95 * self.craft.get_W() / self.craft.get_d()

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

    def calculate_H(self) -> float:
        return max(0.0172 * self.craft.get_L() + 3.653, self.craft.get_h13())
    
    def calculate_Hs(self) -> float:
        return max(0.083 * self.craft.get_L() * self.craft.get_d(), self.craft.get_D() + 1.22) if self.craft.get_L() < 30 else (0.64 * self.calculate_H() + self.craft.get_d())

    
class Acero_Aluminio:

    def __init__(self, craft, zone_pressures):
        self.craft = craft
        self.pressures = zone_pressures
        self.sigma_y = val_data("Esfuerzo ultimo a la tracción (MPa): ")
        self.sigma_u = val_data("Limite elastico por tracción (MPa): ")
        self.zone_results = {}

    # Funcion principal para calcular el plating (Controlador)
    def acero_aluminio_plating(self, zone):
        if zone in [2, 3, 4, 5, 6, 9, 10]:
            pressure, index, s, l = self.pressures.calculate_pressure(zone, context="Plating")
            thickness = max(self.lateral_loading(zone, pressure, index, s, l), self.secondary_stiffening(s), self.minimum_thickness(zone))
            return pressure, thickness
        elif zone in [7, 8]:
            pressure, index, s, l = self.pressures.calculate_pressure(zone, context="Plating")
            thickness = max(self.lateral_loading(zone, pressure, index, s, l), self.secondary_stiffening(s))
            return thickness
        elif zone == 11: #Superestructura
            pressure, index, s, l = self.pressures.calculate_pressure(zone, context="Plating")
            thickness = max(self.lateral_loading(zone, pressure, index, s, l), self.secondary_stiffening(s))
            return thickness
        elif zone == 12: #Waterjets
            pressure, index, s, l = self.pressures.calculate_pressure(zone, context="Plating")
            thickness = max(self.waterjet_tunnels(pressure, index, s, l), self.secondary_stiffening(s))
            return thickness
        elif zone == 13: #Boat Thrusters
            thickness = max(self.boat_thrusters(), self.secondary_stiffening(s))
            return thickness
        elif zone == 14: #Cubiertas de Operación
            thickness = max(self.operation_decks(s, l), self.secondary_stiffening(s))
            return thickness
    
    # Funciones de calculo y auxiliares
    def determine_resistencia(self) -> str: #Revisar
        if self.craft.material == 'Acero':
            if 200 < self.sigma_y < 300:
                return 'Ordinaria'
            elif 300 <= self.sigma_y:
                return 'Alta'
            else:
                return 'Baja'
        else:
            return 'Ordinaria'
    
    def design_stress_plating(self, zone, index) -> float:
        # Asegurarse que sigma_y no sea mayor que 0.7 * sigma u
        sigma = min(self.sigma_y, 0.7 * self.sigma_u)

        if zone in [2, 3, 4]:
            if index == True:
                d_stress = 0.90 * sigma
            else:
                d_stress = 0.55 * sigma
        elif zone in [5, 6, 8, 10, 11]:
            d_stress = 0.60 * sigma
        elif zone == 7:
            d_stress = 0.90 * sigma
        elif zone == 9:
            d_stress = 0.95 * sigma
        elif zone == 12:
            if index == True:
                d_stress = 0.60 * sigma
            else:
                d_stress = 0.55 * sigma
        else:
            d_stress = "No aplicable"
        
        return d_stress
    
    def constant_k(self, s, l) -> float:
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
    
    def constant_k1(self, s, l) -> float:
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
    
    def calculate_beta(a, b, s, l):
        beta_values = {
            1: [
                [0, 1.82, 1.38, 1.12, 0.93, 0.76],
                [1.82, 1.28, 1.08, 0.90, 0.63, 0.63],
                [1.39, 1.07, 0.84, 0.72, 0.52, 0.52],
                [1.12, 0.90, 0.74, 0.60, 0.43, 0.42],
                [0.92, 0.76, 0.62, 0.51, 0.42, 0.36],
                [0.76, 0.63, 0.52, 0.42, 0.35, 0.30]
            ],
            1.4: [
                [0, 2.00, 1.55, 1.20, 0.84, 0.75],
                [1.78, 1.43, 1.23, 0.95, 0.74, 0.63],
                [1.39, 1.13, 1.00, 0.80, 0.62, 0.55],
                [1.12, 0.92, 0.82, 0.68, 0.53, 0.47],
                [0.90, 0.76, 0.68, 0.57, 0.45, 0.38],
                [0.75, 0.62, 0.57, 0.47, 0.38, 0.30]
            ],
            2: [
                [0, 1.64, 1.20, 0.97, 0.78, 0.64],
                [1.73, 1.31, 1.03, 0.80, 0.68, 0.57],
                [1.32, 1.08, 0.88, 0.76, 0.64, 0.50],
                [1.09, 0.90, 0.76, 0.70, 0.64, 0.44],
                [0.87, 0.76, 0.68, 0.64, 0.60, 0.44],
                [0.71, 0.61, 0.63, 0.55, 0.45, 0.38]
            ]
        }

        a_s_indices = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        b_s_indices = {
            1: [0, 0.2, 0.4, 0.6, 0.8, 1.0],
            1.4: [0, 0.2, 0.4, 0.8, 1.2, 1.4],
            2: [0, 0.4, 0.8, 1.2, 1.6, 2.0]
        }

        l_s = l / s
        a_s = a / s
        b_s = b / s

        if l_s >= 2:
            tabla = beta_values[2]
            b_s_idx_array = b_s_indices[2]
        elif abs(l_s - 1.4) < abs(l_s - 1):
            tabla = beta_values[1.4]
            b_s_idx_array = b_s_indices[1.4]
        else:
            tabla = beta_values[1]
            b_s_idx_array = b_s_indices[1]

        a_s_idx = min(range(len(a_s_indices)), key=lambda i: abs(a_s_indices[i] - a_s))
        b_s_idx = min(range(len(b_s_idx_array)), key=lambda i: abs(b_s_idx_array[i] - b_s))

        return tabla[a_s_idx][b_s_idx]
    
    def lateral_loading(self, zone, pressure, index, s, l) -> float:
        k = self.constant_k(s, l)
        sigma_a = self.design_stress_plating(zone, index)
        return s * 10 * np.sqrt((pressure * k)/(1000 * sigma_a))
    
    def secondary_stiffening(self, s) -> float:
        if self.craft.material == 1:
            return 0.01 * s
        else:
            return 0.012 * s
        
    def minimum_thickness(self, zone) -> float:
        resistencia = self.determine_resistencia()
        L = self.craft.get_L()
        if self.craft.material == 1:
            q = 1.0 if resistencia == "Alta" else 245 / self.sigma_y
        else:
            q = 115 / self.sigma_y
        
        if zone == 2:    #Fondo
            if self.craft.material == 1:
                return max(0.44 * np.sqrt(L * q) + 2, 3.5)
            else:
                return max(0.70 * np.sqrt(L * q) + 1, 4.0)
        elif zone in [3, 4]:  #Costados y Espejo
            if self.craft.material == 1:
                return max(0.40 * np.sqrt(L * q) + 2, 3.0)
            else:
                return max(0.62 * np.sqrt(L * q) + 1, 3.5)
        elif zone == 5:  # Strength Deck - Cubierta principal
            if self.craft.material == 1:
                return max(0.40 * np.sqrt(L * q) + 1, 3.0)
            else:
                return max(0.62 * np.sqrt(L * q) + 1, 3.5)
        else: #zone in [6, 9, 10]:  #Lower Decks, W.T. Bulkheads, Deep Tank Bulkheads
            if self.craft.material == 1:
                return max(0.35 * np.sqrt(L * q) + 1, 3.0)
            else:
                return max(0.52 * np.sqrt(L * q) + 1, 3.5)

    def waterjet_tunnels(self, pressure, index, s, l) -> float:
        k = self.constant_k(s, l)
        sigma_a = self.design_stress_plating(12, index)
        return s * np.sqrt((pressure * k) / (1000 * sigma_a))
    
    def boat_thrusters(self) -> float:
        d = self.craft.get_d()
        Q = self.calculate_Q()
        return 0.008 * d * np.sqrt(Q) + 3
    
    def operation_decks(self, s, l) -> float:
        a = val_data("Dimensión de la huella de la rueda, paralela al borde más corto, s, del panel de la placa [mm]: ")
        b = val_data("Dimensión de la huella de la rueda, paralela al borde más largo, l, del panel de la placa [mm]: ")
        d = self.craft.get_d()
        Q = self.calculate_Q(a, b, s, l)
        return 0.008 * d * np.sqrt(Q) + 3


class Alextruido_AlCorrugated:
    
    
    def __init__(self):
        pass


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
    
    
    def __init__(self, craft: Craft):
        self.craft = craft
    
    
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
    
    
    def __init__(self, craft: Craft):
        self.craft = craft

    
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


def cls_factory(craft, zone_pressures):
    # Diccionario que mapea los identificadores de material a clases correspondientes
    plating_classes = {
        1: Acero_Aluminio,
        2: Acero_Aluminio,
        3: Alextruido_AlCorrugated,
        4: Alextruido_AlCorrugated,
        5: Aluminio_Sandwich,
        6: Fibra_Laminada,
        7: Fibra_Sandwich
    }

    # Obtener la clase del diccionario utilizando el identificador de material
    cls = plating_classes.get(craft.material)
    
    return cls(craft, zone_pressures)


def main():
    print("\nESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS\n\n")
    craft = Craft()
    zone_pressures = ZonePressures(craft)
    
    try:
        plating_stiffeners = cls_factory(craft, zone_pressures)
        
        for zone in craft.selected_zones:
            if craft.material in [1, 2]:
                pressure, thickness = plating_stiffeners.acero_aluminio_plating(zone)
                print(f"El espesor de {zone} es: {thickness} [mm], la presion es: {pressure} [MPa]")
            elif craft.material in [3, 4]:
                thickness = plating_stiffeners.calculate_alextruido_alcorrugado(zone, pressure)
                print(f"El espesor de {zone} es: {thickness} [mm], la presion es: {pressure} [MPa]")
            elif craft.material == 5:
                section_modulus, moment_inertia, core_shear_strength = plating_stiffeners.calculate_alsandwich(zone, pressure)
                print(f"""Módulo de sección de {zone} es {section_modulus} [mm^3], la presion es: {pressure} [MPa],
                        el momento de inercía es: {moment_inertia} [mm^4],  el espesor del nucleo: {core_shear_strength} [mm]]""")
            elif craft.material == 6:
                thickness = plating_stiffeners.calculate_fibra_laminada(zone, pressure)
                print(f"El espesor de {zone} es: {thickness} [mm], la presion es: {pressure} [MPa]")
            elif craft.material == 7:
                section_modulus_outer, section_modulus_inner, moment_inertia, core_shear_strength  = plating_stiffeners.calculate_fibra_sandwich(zone, pressure)
                print(f"""Módulo de sección de {zone} de la fibra externa es {section_modulus_outer} [mm^3], de la fibra interna es {section_modulus_inner}\\
                    la presion es: {pressure} [MPa], el momento de inercía es: {moment_inertia} [mm^4], el espesor del nucleo: {core_shear_strength} [mm]]""")
    except ValueError as e:
        print(e)
        
if __name__ == '__main__':
    main()
    

# def main2():
#     print("ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS\n")
#     craft = Craft()
#     material = craft.material
#     for zone in craft.selected_zones:
#         pressure = None if zone in [13, 14] else calculate_pressure(craft, zone)
        
#         thickness, section_modulus, moment_inertia, core_shear_strength, section_modulus_outer, section_modulus_inner = plating(craft, zone, material, pressure)
    
#         print (f"\nEl plating de {zone} es: {plating} [mm], la presion es: {pressure} [MPa]")


# def main3():
#     print("ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS\n")
#     craft = Craft()
#     material = craft.material

#     # Diccionario para seleccionar el objeto de cálculo basado en el material
#     plating_classes = {
#         "Acero": Acero_Aluminio,
#         "Aluminio": Acero_Aluminio,
#         "Aluminio extruido": Alextruido_AlCorrugated,
#         "Aluminio Corrugado": Alextruido_AlCorrugated,
#         "Aluminio en Sandwich": Aluminio_Sandwich,
#         "Fibra Laminada": Fibra_Laminada,
#         "Fibra en sandwich": Fibra_Sandwich
#     }

#     # Crear instancia de plating basada en el material
#     plating = plating_classes[material](craft)
    
#     for zone in craft.selected_zones:
#         pressure = None if zone in [13, 14] else calculate_pressure(craft, zone)
            
#         if material in ["Acero", "Aluminio"]:
#             thickness = plating.calculate_acero_aluminio(zone, pressure)
#         elif material in ["Aluminio extruido", 'Aluminio Corrugado']:
#             thickness = plating.calculate_alextruido_alcorrugado(zone, pressure)
#         elif material == "Aluminio en Sandwich":
#             section_modulus, moment_inertia, core_shear_strength = plating.calculate_alsandwich(zone, pressure)
#         elif material == "Fibra Laminada":
#             thickness = plating.calculate_fibra_laminada(zone, pressure)
#         elif material == "Fibra en sandwich":
#             section_modulus_outer, section_modulus_inner, moment_inertia, core_shear_strength  = plating.calculate_fibra_sandwich(zone, pressure)
        
        
# def main4():
#     print("ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS\n")
#     craft = Craft()
#     material = craft.material
#     for zone in craft.selected_zones:
#         pressure = None if zone in [13, 14] else calculate_pressure(craft, zone)
        
#         if material in ["Acero", "Aluminio"]:
#             plating = Acero_Aluminio(craft, zone, material, pressure)
#             espesor = plating.calculate()
#             print(f"El espesor de {zone} es: {espesor} [mm], la presion es: {pressure} [MPa]")
#         elif material in ["Aluminio extruido", 'Aluminio Corrugado']:
#             plating = Alextruido_AlCorrugated(craft, zone, material, pressure)
#             espesor = plating.calculate()
#             print(f"El espesor de {zone} es: {espesor} [mm], la presion es: {pressure} [MPa]")
#         elif material == "Aluminio en Sandwich":
#             plating = Aluminio_Sandwich(craft, zone, pressure)
#             section_modulus, moment_inertia, core_shear_strength = plating.calculate()
#             print(f"Módulo de sección de {zone} es {section_modulus} [mm^3], la presion es: {pressure} [MPa],\\
#                     el momento de inercía es: {moment_inertia} [mm^4],  el espesor del nucleo: {core_shear_strength} [mm]]")
#         elif material == "Fibra Laminada":
#             plating = Fibra_Laminada(craft, zone, pressure)
#             espesor = plating.calculate()
#             print(f"El espesor de {zone} es: {espesor} [mm], la presion es: {pressure} [MPa]")
#         elif material == "Fibra en sandwich":
#             plating = Fibra_Sandwich(craft, zone, pressure)
#             section_modulus_outer, section_modulus_inner, moment_inertia, core_shear_strength  = plating.calculate()
#             print(f"Módulo de sección de {zone} de la fibra externa es {section_modulus_outer} [mm^3], de la fibra interna es {section_modulus_inner}\\
#                 la presion es: {pressure} [MPa], el momento de inercía es: {moment_inertia} [mm^4], el espesor del nucleo: {core_shear_strength} [mm]]")

# def main5():
#     print("ESCANTILLONDAO ABS-HSC - ABS-HSC SCANTLINGS\n")
#     craft = Craft()
#     material = craft.material
    
#     if material in ["Acero", "Aluminio"]:
#         plating = Acero_Aluminio(craft, zone, material, pressure)
#     elif material in ["Aluminio extruido", 'Aluminio Corrugado']:
#         plating = Alextruido_AlCorrugated(craft, zone, material, pressure)
#     elif material == "Aluminio en Sandwich":
#         plating = Aluminio_Sandwich(craft, zone, pressure)
#     elif material == "Fibra Laminada":
#         plating = Fibra_Laminada(craft, zone, pressure)
#     elif material == "Fibra en sandwich":
#         plating = Fibra_Sandwich(craft, zone, pressure)
    
    
#     for zone in craft.selected_zones:
#         pressures_list = []
#         pressure = None if zone in [13, 14] else calculate_pressure(craft, zone)
#         pressures_list.append(pressure)
    
