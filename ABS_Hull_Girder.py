"""
¿Que es Hull Girder Strength y como se traduce al español?

La norma ABS referente a embarcaciones de alta velocidad cuando menciona "hull girder strength" se refiere 
a la resistencia estructural longitudinal del casco del barco.

En la ingeniería naval, el "hull girder" o vagra maestra del casco, es una manera conceptual de representar al 
casco como una gran viga que soporta diversas cargas mientras navega. Estas cargas incluyen el peso del barco,
la carga que transporta, el impacto de las olas, y las tensiones de flexión y torsión durante la navegación.

La "resistencia longitudinal del casco" se evalúa para asegurar que el barco puede soportar estas cargas sin 
flexionarse o torcerse más allá de los límites seguros. Esta evaluación es crucial para garantizar la seguridad 
y la integridad estructural del barco durante su operación.

En español, "hull girder strength" se traduciría literalmente como "resistencia de la vagra maestra del casco".
"""


from ABS_Craft import Craft
from math import sqrt, pow


class Hull_Girder:
    def __init__(self, craft: Craft) -> None:
        self.craft = craft
        # Atributos internos para almacenar valores
        self.C1 = self.calculate_C1()
        self.C2 = 0.01
        self.Cb = self.calculate_Cb()
        self.K3 = self.calculate_K3()
        self.C = self.calculate_C()
        self.Q = self.calculate_Q()
        self.K = self.calculate_K()
        self.Hull_Girder_SM = self.SM()
        self.Hull_Girder_I = self.M_inercia()

    def calculate_C1(self) -> float:
        if self.craft.L < 90:
            return 0.044 * self.craft.L + 3.75
        else:  # L >= 90
            return 10.75 - pow(((300 - self.craft.L) / 100), 1.5)

    def calculate_Cb(self) -> float:
        if self.craft.L < 35:
            return 0.45
        elif self.craft.L >= 61:
            return 0.6
        else:
            return 0.45 + (0.6 - 0.45) * ((self.craft.L - 35) / (61 - 35))

    def calculate_K3(self) -> float:
        return max(1.0, min(0.70 + 0.30 * ((self.craft.V / sqrt(self.craft.L)) / 2.36), 1.30))

    def calculate_C(self) -> float:
        if self.craft.material == "Acero":
            return 1.0
        elif self.craft.material == "Aluminio":
            return 0.90
        elif self.craft.material in ('Fibra laminada', 'Fibra en sandwich'):
            return 0.80
        else:
            raise ValueError(
                f"El material {self.craft.material}, no se encuentra en la base de datos")

    def calculate_Q(self) -> float:
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
                if (min_yield <= self.craft.sigma_y <= max_yield) and (min_tensile <= self.craft.sigma_u <= max_tensile):
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
                return 490 / (min(self.craft.sigma_y, 0.7 * self.craft.sigma_u) + 0.66 * self.craft.sigma_u)

        elif self.craft.material == "Aluminio":
            sigma_y = min(self.craft.sigma_y, 0.7 * self.craft.sigma_u)
            q5 = 115 / sigma_y
            Qo = 635 / (sigma_y + self.craft.sigma_u)
            return max(0.9 + q5, Qo)

        elif self.craft.material in ('Fibra laminada', 'Fibra en sandwich'):
            return 400 / (0.75 * self.craft.sigma_u)
        else:
            raise ValueError(
                f"El material {self.craft.material}, no se encuentra en la base de datos")

    #   Modulo de Seccion de la Vagra Maestra
    def SM(self) -> float:
        return self.C1 * self.C2 * pow(self.craft.L, 2) * self.craft.B * (self.Cb + 0.7) * self.K3 * self.C * self.Q

    # Momento de Inercia de la Vagra Maestra
    def calculate_K(self) -> float:
        Matriz_coeficientes = [[50, 13.33, 1.8],  # i: tipo de servicio
                               [40, 13.33, 1.8],  # j: material
                               [33.3, 11.1, 1.5]]
        if self.craft.L <= 61:
            i = 1  # "Unrestricted Service L <= 61"
            if self.craft.material == 'Acero':
                j = 0
            elif self.craft.material == 'Aluminio':
                j = 1
            elif self.craft.material in ('Fibra laminada', 'Fibra en sandwich'):
                j = 2
            else:
                raise ValueError(
                    f"El material {self.craft.material}, no se encuentra en la base de datos")
            return Matriz_coeficientes[i][j]
        else:
            i = 2  # "All Craft L > 61"
            if self.craft.material == 'Acero':
                j = 0
            elif self.craft.material == 'Aluminio':
                j = 1
            elif self.craft.material in ('Fibra laminada', 'Fibra en sandwich'):
                j = 2
            else:
                raise ValueError(
                    f"El material {self.craft.material}, no se encuentra en la base de datos")
            return Matriz_coeficientes[i][j]

    def M_inercia(self) -> float:
        return float((self.craft.L / (self.Q * self.C)) * (self.Hull_Girder_SM / self.K))
