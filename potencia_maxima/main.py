from ABS_HSC.validations import val_data


class Craft_1:  # Norma ISO 11592-1

    def __init__(self, LH, Bt, Vmax, B04, tipo_direccion):
        self.LH = LH
        self.Bt = Bt
        self.Vmax = Vmax
        self.B04 = B04
        self.tipo_direccion = tipo_direccion
 
    def potencia_maxima_distancia_ref(self):
        D = 6 * self.LH if self.Vmax <= 30 else 6 * self.LH + 2 * (self.Vmax - 30)
        if self.Vmax > 7 * (self.LH**0.5):
            landa = self.LH * self.Bt
            if landa <= 5.1:
                if self.B04 < 5:
                    p_max = 6 * landa - 18.1
                else:
                    p_max = 5.4762 * landa - 12.929
            else:
                if self.tipo_direccion == 1:  # Con rueda de dirección remota
                    p_max = 16 * landa - 67
                elif self.tipo_direccion == 2 and self.B04 < 5:
                    p_max = (4.2 * landa - 11)  # Sin rueda de dirección remota, ángulo < 5
                else:
                    p_max = (6.4 * landa - 19)  # Sin rueda de dirección remota, ángulo ≥ 5
        else:
            p_max = "La potencia del motor, a opción del fabricante de la embarcación, será la máxima potencia de propulsión de la embarcación."
        return p_max, D


class Craft_2:  # Norma ISO 11592-2

    def __init__(self, LH, LWL, Vmax):
        self.LH = LH
        self.LWL = LWL
        self.Vmax = Vmax
        self.g = 9.8
        self.Vtmax = min(3 * self.LH + 24, 70)
        self.Fn = self.Vmax / ((self.g * self.LWL)**0.5)

    def potencia_maxima_distancia_ref(self):
        if 8 <= self.LH <= 24:
            D = (6 * self.LH if self.Vmax <= 30 else 6 * self.LH + (0.1 * self.LH + 1.2) * (min(self.Vmax, self.Vtmax) - 30))
            if self.Fn < 1.1:
                p_max = "La norma no cobija a embarcaciones con número Froude menos a 1.1"
            else:
                p_max = "La potencia nominal máxima de propulsión se debe  obtener utilizando los resultados de los ensayos  especificados  en  los  capítulos  6  y  7."
        else:
            raise ValueError("La eslora del casco de su embarcación no aplica a la norma ISO 11592-2.")
        return p_max, D


def main():
    try:
        LH = val_data("Ingrese la eslora del casco (LH) en metros: ")
        Vmax = val_data("Ingrese la velocidad máxima de la embarcación (Vmax) en nudos: ")

        if LH < 8:
            Bt = val_data("Ingrese la manga del espejo (Bt) en metros: ")
            B04 = val_data(
                "Ingrese el ángulo de astilla muerta (B04) en grados: ")
            tipo_direccion = val_data("Seleccione el tipo de dirección de la embarcación \n1. Dirección con volante en consola\n2. Dirección con brazo del motor manual\n-> ", False, True, -1, 1, 2,)
            embarcacion = Craft_1(LH, Bt, Vmax, B04, tipo_direccion)
        else:
            LWL = val_data("Ingrese la eslora de la línea de flotación (LWL) en metros: ", True, True, -1, 0.1, LH)
            embarcacion = Craft_2(LH, LWL, Vmax)

        potencia_maxima, distancia_referencia = (
            embarcacion.potencia_maxima_distancia_ref())
        print(f"La potencia nominal máxima de propulsión es {potencia_maxima} y la distancia de referencia es {distancia_referencia} metros.")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
