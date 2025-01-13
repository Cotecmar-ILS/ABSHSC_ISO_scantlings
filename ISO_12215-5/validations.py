from typing import Optional, Union

from typing import Optional, Union

def val_data(
    texto: str,
    is_float: bool = True,
    is_positive: bool = True,
    default_value: Optional[Union[int, float, str]] = -1,
    range_min: Optional[Union[int, float]] = None,
    range_max: Optional[Union[int, float]] = None,
    allowed_values: Optional[list[Union[int, float, str]]] = None,
) -> Union[int, float, str]:
    """
    Valida y convierte el valor ingresado por el usuario según los parámetros especificados.
    """
    while True:
        try:
            # Verificación y reemplazo inicial
            valor = input(texto).strip().replace(',', '.')

            # Verificación de caracteres no válidos
            if '_' in valor:
                raise ValueError("El valor ingresado contiene caracteres no válidos.\n")

            # Si el valor ingresado está vacío
            if not valor and default_value is not None:
                return float(default_value) if is_float else int(default_value)
            elif not valor:
                print("Error: Debe ingresar un valor.\n")
                continue

            # Conversión a float o int
            valor = float(valor) if is_float else int(valor)

            # Validaciones
            error_msgs = []
            if is_positive and valor <= 0 and (allowed_values is None or valor not in allowed_values):
                error_msgs.append("El valor debe ser positivo.")
            if range_min is not None and valor < range_min:
                error_msgs.append(f"El valor debe ser mayor o igual a {range_min}.")
            if range_max is not None and valor > range_max:
                error_msgs.append(f"El valor debe ser menor o igual a {range_max}.")
            if allowed_values is not None and valor not in allowed_values:
                error_msgs.append("El valor no está permitido.")

            if error_msgs:
                print("Error: " + " ".join(error_msgs) + "\n")
                continue

            return valor
        except ValueError as e:
            print(f"Error: {str(e)}. Intente nuevamente.\n")
