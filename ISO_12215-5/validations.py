from typing import Optional, Union

def val_data(
    texto: str,
    is_float: bool = True,
    default_value: Optional[Union[int, float, str]] = -1,
    range_min: Optional[Union[int, float]] = None,
    range_max: Optional[Union[int, float]] = None,
    allowed_values: Optional[list[Union[int, float, str]]] = None,
) -> Union[int, float, str]:
    """
    Valida y convierte el valor ingresado por el usuario según los parámetros especificados.

    Args:
        texto (str): Mensaje mostrado al usuario.
        is_float (bool): Si el valor esperado es un número decimal. Default es True.
        default_value (int | float | str): Valor por defecto si el usuario no ingresa uno.
        range_min (int | float): Valor mínimo permitido. Default es None.
        range_max (int | float): Valor máximo permitido. Default es None.
        allowed_values (list): Lista de valores permitidos. Default es None.

    Returns:
        int | float | str: El valor ingresado validado.
    """
    while True:
        try:
            # Solicitar y preparar la entrada
            valor = input(texto).strip().replace(',', '.')

            # Verificar si se debe usar el valor por defecto
            if not valor and default_value is not None:
                return float(default_value) if is_float else int(default_value)
            elif not valor:
                print("Error: Debe ingresar un valor.\n")
                continue

            # Convertir a float o int según corresponda
            valor = float(valor) if is_float else int(valor)

            # Lista de errores acumulados
            error_msgs = []

            # Validar valores permitidos
            if allowed_values is not None and valor in allowed_values:
                # Si está en los valores permitidos, no es necesario validar rangos.
                return valor
            else:
                # Validar rango mínimo
                if range_min is not None and valor < range_min:
                    error_msgs.append(f"El valor debe ser mayor o igual a {range_min}.")
                # Validar rango máximo
                if range_max is not None and valor > range_max:
                    error_msgs.append(f"El valor debe ser menor o igual a {range_max}.")

            # Si hay errores, mostrarlos
            if error_msgs:
                print("Error: " + " ".join(error_msgs) + "\n")
                continue

            # Si pasa todas las validaciones, retornarlo
            return valor

        except ValueError as e:
            print(f"Error: {str(e)}. Intente nuevamente.\n")
