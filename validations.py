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

    Parámetros:
        texto (str): El texto que se muestra al usuario para solicitar el valor.
        is_float (bool, opcional): Indica si se espera un valor decimal (float). Por defecto True.
        is_positive (bool, opcional): Indica si el valor debe ser positivo y mayor a 0. Por defecto True.
        default_value (int o float, opcional): Valor por defecto tomado si el usuario no ingresa nada. Por defecto -1.
        range_min (int o float, opcional): Valor mínimo permitido. Por defecto None.
        range_max (int o float, opcional): Valor máximo permitido. Por defecto None.
        allowed_values (list, opcional): Lista de valores permitidos. Por defecto None.

    Ejemplo:
        valor = val_datos("Ingrese un número: ", is_float=True, is_positive=True, default_value=5.0, range_min=0.1, range_max=10.0, allowed_values=[1, 2, 3, 5, 8])
        print("Valor ingresado:", valor)

    Retorna:
        float: El valor numérico validado y convertido. Si el usuario no ingresa un valor, se retorna el valor por defecto si está especificado.
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
                return default_value
            elif not valor:
                print("Error: Debe ingresar un valor.\n")
                continue

            # Conversión a float o int
            valor = float(valor) if is_float else int(valor)

            # Validaciones
            if is_positive and valor <= 0:
                error_msg = "El valor ingresado debe ser un número real positivo mayor a 0\n"
            elif range_min is not None and valor < range_min:
                error_msg = f"El valor ingresado debe ser mayor o igual a {range_min}\n"
            elif range_max is not None and valor > range_max:
                error_msg = f"El valor ingresado debe ser menor o igual a {range_max}\n"
            elif allowed_values is not None and valor not in allowed_values:
                error_msg = "El valor ingresado no está permitido.\n"
            else:
                return valor

            print(f"Error: {error_msg}\n")
        except ValueError as e:
            print(f"Error: {str(e)}. Intente nuevamente.\n")