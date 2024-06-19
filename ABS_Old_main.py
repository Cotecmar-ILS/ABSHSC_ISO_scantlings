# from ABS_Craft import Craft
# from ABS_Hull_Girder import Hull_Girder
# from ABS_Bottom import Bottom
# from ABS_Side import Side

# def main():
#     #Crear una instancia de la clase
#     craft = Craft()
#     if craft.zone == 'Cuaderna Maestra':
#         hull_girder = Hull_Girder(craft)
#         print(f"\nC1:{hull_girder.C1}, C2:{hull_girder.C2}, Cb:{hull_girder.Cb}, K3:{hull_girder.K3}, C:{hull_girder.C}, Q:{hull_girder.Q}, K:{hull_girder.K}")
#         print(f"\nEl Modulo de Sección de la cuaderna maestra no debe ser menor a: {hull_girder.Hull_Girder_SM} [cm^2 - m] y el Momento de Inercia no debe ser menor a: {hull_girder.Hull_Girder_I} [cm^2 - m^2]")
#     elif craft.zone == 'Fondo':
#         bottom = Bottom(craft)
#         print(f"\nh13:{bottom.h13}, ncg:{bottom.ncg}, FV:{bottom.FV}, k:{bottom.k}, sigma_ap:{bottom.sigma_ap}, d_stress:{bottom.d_stressp}, qa:{bottom.q}")
#         print(f"FDp:{bottom.FDp}, Pressure_p:{bottom.bottom_p_p}")
#         print(f"FDs:{bottom.FDs}, Pressure_s:{bottom.bottom_p_s}")
#         print(f"\nEl espesor de las laminas del fondo calculado es: {bottom.bottom_t:.5f} [mm]")
#         print(f"\nK4:{bottom.K4}, E:{bottom.E}")
#         print(f"\nEl modulo de seccion minimo para los longitudinales del fondo es de: {bottom.binternals_SM[0]:.5f} [cm^3], y para los transverslaes es de: {bottom.binternals_SM[1]:.5f} [cm^3] y la Inercia no debe ser menor a: {bottom.binternals_I:.5f} [cm^4]")
#     elif craft.zone == 'Costado':
#         side = Side(craft)
#         print(f"\nh13:{side.h13}, ncg:{side.ncg}, FV:{side.FV}, k:{side.k}, sigma_ap:{side.sigma_ap}, d_stress:{side.d_stressp}, qa:{side.q}")
#         print(f"FDp:{side.FDp}, Pressure_p:{side.side_p_p}")
#         print(f"FDs:{side.FDs}, Pressure_s:{side.side_p_s}")
#         print(f"\nEl espesor de las laminas del costado calculado es: {side.side_t:.5f} [mm]")
#         print(f"\nK4:{side.K4}, E:{side.E}")
#         print(f"\nEl modulo de seccion minimo para los longitudinales del costado es de: {side.binternals_SM[0]:.5f} [cm^3], y para los transverslaes es de: {side.binternals_SM[1]:.5f} [cm^3] y la Inercia no debe ser menor a: {side.binternals_I:.5f} [cm^4]")

# if __name__ == "__main__":
#     main()
