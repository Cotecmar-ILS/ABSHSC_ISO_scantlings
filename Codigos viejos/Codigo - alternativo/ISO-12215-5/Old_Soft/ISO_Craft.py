from validations import val_data
from typing import Tuple, List
from math import sqrt, pow

class Craft:

    PLATING_MATERIALS: List[str] = ['Acero', 'Aluminio', 'FRP-Single Skin', 'FRP-Sandwich']
    #STIFFENING_MATERIALS: List[str] = ['Acero', 'Aluminio', 'FRP']#, 'Madera laminada', 'Madera maciza', 'Madera contrachapada']
    ZONES: List[str] = ['Fondo', 'Costado', 'Cubierta', 'Superestructuras, Mamparos Estancos y Estructurales y Fronteras de Tanques']
    SKIN_TYPE: List[str] = ['Fibra de vidrio E con filamentos cortados', 'Fibra de vidrio tejida', 'Fibra tejida de carbono, aramida(kevlar) o híbrida']
    SANDWICH_CORE: List[str] = ['Madera Balsa', 'Núcleo con alargamiento a la rotura < 35 % (PVC reticulado, etc.)', 'Núcleo con alargamiento de rotura > 35 % (PVC lineal, SAN, etc.)', 'Nucleo Tipo Panal']

    def __init__(self) -> None:
        print("\nCalculadora de Escantillones - 'Scantlings Calculator'\n")
        self.LH, self.LWL, self.BWL, self.BC, self.V, self.mLDC, self.B04 = self.general_attributes()
        self.type = 'Displacement' if (self.V/sqrt(self.LWL)) < 5 else 'Planning'
        self.category = self.ship_category()
        self.zone = self.select_zone()
        self.material = self.select_materials()
        self.skin = self.skin_type() if self.material in ['FRP-Single Skin', 'FRP-Sandwich'] else None
        self.kDC = self._calculate_kDC()
        self.nCG = self._calculate_ncg()
        self.sigma_u, self.sigma_y, self.sigma_uf, self.sigma_ut, self.sigma_uc, self.tau_u, self.tau_nu, self.Eio = self.input_stresses()
        self.sigma_dp, self.sigma_dtp, self.sigma_dcp, self.tau_dp = self.design_stresses_plating()
        self.sigma_ds, self.tau_ds = self.design_stresses_stiffeners()
        self.kSA = 5

    def display_menu(self, items: List[str]) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def general_attributes(self) -> Tuple[float]:
        LH = val_data("\nIngrese la eslora maxima 'LH' de su embarcación (metros): ", True, True, 0, 2.5, 24)
        LWL = val_data("Ingrese la eslora de la linea de flotación o eslora de escantillón 'LWL' (metros): ", True, True, LH, 2.5, LH)
        BWL = val_data("Ingrese la manga de la linea de flotación 'BWL' (metros): ")
        BC = val_data("Ingrese la manga del lomo o 'chine' 'BC' (metros): ", True, True, BWL)
        V = val_data("Ingrese la velocidad maxima de diseño 'V' de la embarcación (Nudos): ", True, True, 0, 2.36 * sqrt(LWL)) 
        mLDC = val_data("Ingrese el desplazamiento de la embarcación 'mLDC' (Toneladas): ") * 1000 
        B04 = val_data(f"Ingrese el ángulo de astilla muerta 'B04' en el LCG, o a {0.4*LWL:.3f} metros de la popa (°grados): ")  #Mire ISO-12215-5 figure 1 - cap 6, sec 6.1
        return LH, LWL, BWL, BC, V, mLDC, B04

    def ship_category(self) -> str:
        print("\nSeleccione la categoria para el diseño de su embarcación:")
        print("1. Categoria A (Oceano)\n2. Categoría B ('Offshore')\n3. Categoría C ('Inshore')\n4. Categoría D (Aguas protegidas)")
        select = val_data("\nIngrese el numero correspondiente: ", False, True, 0, 1, 4)
        if select == 1:
            category = 'A'
        elif select == 2:
            category = 'B'
        elif select == 3:
            category = 'C'
        elif select == 4:
            category = 'D'
        else:
            raise ValueError(f"Numero Sleccionado: {select}, no reconocido") 
        return category

    def select_materials(self) -> str:
        print("\nSeleccione el material para el escantillonado de su embarcación")
        self.display_menu(self.ISO_MATERIALS)
        choice1 = val_data("\nIngrese el numero correspondiente: ", False, True, 0, 1, len(self.PLATING_MATERIALS))
        # print("\nSeleccione el material para los elementos de refuerzo de su embarcación")
        # self.display_menu(self.STIFFENING_MATERIALS)
        # choice2 = val_data("\nIngrese el numero correspondiente: ", False, True, 0, 1, len(self.STIFFENING_MATERIALS))
        return self.PLATING_MATERIALS[choice1 - 1]#, self.STIFFENING_MATERIALS[choice2 - 1]

    def select_zone(self) -> str:
        """Permite al usuario seleccionar una zona."""
        print("\nSeleccione la zona donde desea realizar los calculos")
        self.display_menu(self.ZONES)
        choice = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.ZONES))
        return self.ZONES[choice - 1]

    def _calculate_kDC(self) -> float:
        if self.category == 'A':
            kDC = 1
        elif self.category == 'B':
            kDC = 0.8
        elif self.category == 'C':
            kDC = 0.6
        else:
           kDC = 0.4
        return kDC

    def _calculate_ncg(self) -> float:
        nCG = 0.32 * ((self.LWL / (10 * self.BC)) + 0.084) * (50 - self.B04) * ((pow(self.V, 2) * pow(self.BC, 2)) / self.mLDC)
        if nCG > 3:
            nCG = (0.5 * self.V) / (pow(self.mLDC, 0.17))
        if nCG > 7:
            print(f"\nCUIDADO: El valor de carga dinámica (nCG)= {nCG} no debe ser mayor a 7, revise sus parametros iniciales")
        return nCG

    def input_stresses(self) -> Tuple:
        sigma_u = sigma_y = sigma_uf = Eio = sigma_ut = sigma_uc = tau_u = tau_nu = None
        if self.material in ['Acero', 'Aluminio']:
            sigma_u = val_data(f"\nIngrese la resistencia última a la tracción 'sigma_u' del {self.material} en (MPa): ")
            sigma_y = val_data(f"Ingrese el límite elástico por tracción del {self.material} en (MPa): ", True, True, sigma_u, 0, sigma_u)
        elif self.material == 'FRP-Single Skin':
            sigma_uf = val_data("\nIngrese la resistencia última a la flexión (MPa): ")
            sigma_ut = val_data("Ingrese la resistencia última de tensión del laminado (MPa): ")
            sigma_uc = val_data("Ingrese la resistencia última de compresión del laminado (MPa): ")
            tau_u = val_data("Ingrese la resistencia última al cortante de la fibra (MPa): ")
            Eio = val_data("Ingrese el Módulo de Elasticidad de la fibra (MPa): ")
        elif self.material == 'FRP-Sandwich':
            sigma_ut = val_data("\nIngrese la resistencia última de tensión del laminado exterior (MPa): ")
            sigma_uc = val_data("Ingrese la resistencia última de compresión del laminado interior (MPa): ")
            tau_u = val_data("Ingrese la resistencia última al cortante de la fibra (MPa): ")
            tau_nu = val_data("Ingrese la resistencia última al cortante del nucleo (MPa): ")
            Ei = val_data("Ingrese el Módulo de elasticidad de la fibra interna (MPa): ")
            Eo = val_data("Ingrese el Módulo de elasticidad de la fibra externa (MPa): ")
            Eio = max(Ei, Eo)
        else:
            raise ValueError(f"Material '{self.material}' no reconocido")
        return sigma_u, sigma_y, sigma_uf, sigma_ut, sigma_uc, tau_u, tau_nu, Eio

    def design_stresses_plating(self) -> Tuple:
        sigma_d = sigma_dt = sigma_dc = tau_dp = None
        if self.material == 'Acero' or self.material == 'Aluminio':
            sigma_d = min(0.6 * self.sigma_u, 0.9 * self.sigma_y)
        elif self.material == 'FRP-Single Skin':
            sigma_d = 0.5 * self.sigma_uf
        elif self.material == 'FRP-Sandwich':
            sigma_dt = 0.5 * self.sigma_ut
            sigma_dc = 0.5 * self.sigma_uc  # min(... , 0.3 * pow(self.craft.Ec * self.craft.Eco * self.craft.Gc, 1/3))
            if self.LH < 10:
                tau_dp = max(0.25, self.tau_nu * 0.5)
            elif 10 <= self.LWL <= 15:
                tau_dp = max(0.25 + 0.03 * (self.LH -10), self.tau_nu * 0.5)
            else:
                tau_dp = max(0.40, self.tau_nu * 0.5)
        else:
            raise ValueError(f"Material '{self.material}' no reconocido")
        return sigma_d, sigma_dt, sigma_dc, tau_dp

    def design_stresses_stiffeners(self) -> Tuple:
        if self.material == 'Aluminio':
            sigma_d = 0.7 * self.sigma_y
            tau_ds = 0.4 * self.sigma_y
        elif self.material == 'Acero':
            sigma_d = 0.8 * self.sigma_y
            tau_ds = max(0.58 * self.sigma_y, 0.45 * self.sigma_y)
        elif self.material in ['FRP-Single Skin', 'FRP-Sandwich']:
            sigma_d = max(0.5 * self.sigma_ut, 0.5 * self.sigma_uc)
            tau_ds = 0.5 * self.tau_u
        else:
            raise ValueError(f"Material '{self.material}' no reconocido")
        return sigma_d, tau_ds

    def skin_type(self) -> str:
        print("\nSeleccione el tipo de fibra de diseño")
        self.display_menu(self.SKIN_TYPE)
        choice = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.SKIN_TYPE))
        return self.SKIN_TYPE[choice - 1]
