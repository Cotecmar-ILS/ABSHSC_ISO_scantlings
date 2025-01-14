from typing import Optional, Union

def val_data(
    texto: str,
    range_min: Optional[Union[int, float]] = 1e-6,  # Valor mínimo predeterminado (positivo)
    range_max: Optional[Union[int, float]] = None,  # Sin límite máximo por defecto
    default_value: Optional[Union[int, float, str]] = None,  # Sin valor por defecto
    is_float: bool = True,
    allowed_values: Optional[list[Union[int, float, str]]] = None,  # Sin valores permitidos específicos por defecto
) -> Union[int, float, str]:
    """
    Valida y convierte el valor ingresado por el usuario según los parámetros especificados.

    Args:
        texto (str): Mensaje mostrado al usuario.
        range_min (float): Valor mínimo permitido. Default es 1e-6 (positivo y mayor que cero).
        range_max (float | None): Valor máximo permitido. Default es None (sin límite).
        is_float (bool): Si el valor esperado es un número decimal. Default es True.
        default_value (int | float | str | None): Valor por defecto si el usuario no ingresa uno.
        allowed_values (list | None): Lista de valores permitidos. Default es None (sin restricciones).

    Returns:
        int | float | str: El valor ingresado validado.
    """
    while True:
        try:
            # Solicitar entrada y preparar el valor
            valor = input(texto).strip().replace(',', '.')

            # Si el valor está vacío, usar default_value si está definido
            if not valor:
                if default_value is not None:
                    return float(default_value) if is_float else int(default_value)
                else:
                    print("Debe ingresar un valor. Inténtelo nuevamente.\n")
                    continue

            # Validar si el valor ingresado está en la lista de valores permitidos antes de la conversión
            if allowed_values is not None and valor in map(str, allowed_values):
                return float(valor) if is_float else int(valor)

            # Validar si el valor ingresado es un número y convertirlo
            if is_float:
                valor = float(valor)  # Convertir directamente a float si se permite
            elif '.' in valor:
                # Si no se permite float pero hay un punto decimal, mostrar error
                print("Error: Se esperaba un número entero. Por favor, ingrese un valor válido.\n")
                continue
            else:
                valor = int(valor)  # Convertir a int si no hay punto decimal

            # Validaciones de rango
            error_msgs = []
            if range_min is not None and valor < range_min:
                # Si range_min > 0, mostrar un mensaje claro
                if range_min == 1e-6:
                    error_msgs.append("El valor debe ser mayor a 0.")
                else:
                    error_msgs.append(f"El valor debe ser mayor o igual a {range_min}.")
            if range_max is not None and valor > range_max:
                error_msgs.append(f"El valor debe ser menor o igual a {range_max}.")

            # Mostrar errores acumulados o retornar el valor
            if error_msgs:
                print("Error: " + " ".join(error_msgs) + "\n")
            else:
                return valor

        except ValueError:
            # Mensaje claro para valores no numéricos
            print("Error: El valor ingresado no es numérico. Por favor, ingrese un número válido.\n")
