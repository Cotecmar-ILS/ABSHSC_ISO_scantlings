from ISO_Craft import Craft
from ISO_Bottom import Bottom
from ISO_Side import Side
from ISO_Deck import Deck
#from ISO_SDBI import SDBI

def main():
    #Crear una instancia de la clase
    craft = Craft()
    if craft.zone == 'Fondo':
        bottom = Bottom(craft)
        # print(f"\ntype:{craft.type}, category:{craft.category}, zone:{craft.zone}, kDC:{craft.kDC}, nCG:{craft.nCG}, material:{craft.material}, esf.diseño_p:{craft.sigma_dp}, esf.diseño_s:{craft.sigma_ds}, esf.diseño_cortante_s:{craft.tau_ds}, kSA:{craft.kSA}")
        # print(f"\nxp:{bottom.xp}, kLp:{bottom.kLp}, kRp:{bottom.kRp}, ADp:{bottom.ADp}, kARp:{bottom.kARp}, PBMDp:{bottom.PBMDp}, PBMPp:{bottom.PBMPp}, Min.Bottom Pressure:{bottom.PBM_MIN}, Bottom Pressure_p:{bottom.bottom_pressure_p}, k2:{bottom.k2}, k3:{bottom.k3}, kC:{bottom.kC}")
        # print(f"\nxs:{bottom.xs}, kLs:{bottom.kLs}, kRs:{bottom.kRs}, ADs:{bottom.ADs}, kARs:{bottom.kARs}, PBMDs:{bottom.PBMDs}, PBMPs:{bottom.PBMPs}, Min.Bottom Pressure:{bottom.PBM_MIN}, Bottom Pressure_s:{bottom.bottom_pressure_s}, kCS:{bottom.kCS}")
        print(f"\nEl espesor de las láminas del fondo calculado es: {bottom.t:.5f} [mm]")
        if craft.material == 'FRP-Single Skin':
            print(f"Peso mínimo que debe tener la fibra seca es de: {bottom.w_min} [kg/m^2]")
        elif craft.material == 'FRP-Sandwich':
            print(f"Peso mínimo de la fibra seca exterior: {bottom.wos} [kg/m^2], Peso minimo de la fibra interior: {bottom.wis} [kg/m^2]")
            print(f"El Módulo de sección mínimo requerido de la piel exterior para un laminado sándwich de 1 cm de ancho es de: {bottom.SM_0} [cm^3/cm], y para el laminado interior es de: {bottom.SM_1} [cm^3/cm]")
        print(f"\nEl módulo de sección mínimo para los refuerzos del fondo es de: {bottom.SM:.5f} [cm^3], y el Area del alma minima es de: {bottom.AW:.5f} [cm^2]")
        print(f"Adicionalmente, el Segundo Momento de Inercia mínimo requerido para los refuerzos es de {bottom.second_I} [cm^4]") if craft.material in ['FRP-Single Skin', 'FRP-Sandwich'] else None
    elif craft.zone == 'Costado':
        side = Side(craft)
        # print(f"\ntype:{craft.type}, category:{craft.category}, zone:{craft.zone}, kDC:{craft.kDC}, nCG:{craft.nCG}, material:{craft.material}, esf.diseño_p:{craft.sigma_dp}, esf.diseño_s:{craft.sigma_ds}, esf.diseño_cortante_s:{craft.tau_ds}, kSA:{craft.kSA}")
        # print(f"\nxp:{side.xp}, kLp:{side.kLp}, kRp:{side.kRp}, ADp:{side.ADp}, kARp:{side.kARp}, kZp:{side.kZp}, PSMDp:{side.PSMDp}, PBMPp:{side.PSMPp}, Min.side Pressure:{side.PSM_MIN}, side Pressure_p:{side.side_pressure_p}, k2:{side.k2}, k3:{side.k3}, kC:{side.kC}")
        # print(f"\nxs:{side.xs}, kLs:{side.kLs}, kRs:{side.kRs}, ADs:{side.ADs}, kARs:{side.kARs}, PBMDs:{side.PSMDs}, PBMPs:{side.PSMPs}, Min.side Pressure:{side.PSM_MIN}, side Pressure_s:{side.side_pressure_s}, kCS:{side.kCS}")
        print(f"\nEl espesor de las láminas del costado calculado es: {side.t:.5f} [mm]")
        if craft.material == 'FRP-Single Skin':
            print(f"Peso mínimo que debe tener la fibra seca es de: {side.w_min} [kg/m^2]")
        elif craft.material == 'FRP-Sandwich':
            print(f"Peso mínimo de la fibra seca exterior: {side.wos} [kg/m^2], Peso minimo de la fibra interior: {side.wis} [kg/m^2]")
            print(f"El Módulo de sección mínimo requerido de la piel exterior para un laminado sándwich de 1 cm de ancho es de: {side.SM_0} [cm^3/cm], y para el laminado interior es de: {side.SM_1} [cm^3/cm]")
        print(f"\nEl Area del alma minima es de: {side.AW:.5f} [cm^2], y el módulo de sección mínimo para los refuerzos del costado es de: {side.SM:.5f} [cm^3]")
        print(f"Adicionalmente, el Segundo Momento de Inercia mínimo requerido para los refuerzos es de {side.second_I} [cm^4]") if craft.material in ['FRP-Single Skin', 'FRP-Sandwich'] else None
    elif craft.zone == 'Cubierta':
        deck = Deck(craft)
        # print(f"\ntype:{craft.type}, category:{craft.category}, zone:{craft.zone}, kDC:{craft.kDC}, nCG:{craft.nCG}, material:{craft.material}, esf.diseño_p:{craft.sigma_dp}, esf.diseño_s:{craft.sigma_ds}, esf.diseño_cortante_s:{craft.tau_ds}, kSA:{craft.kSA}")
        # print(f"\nxp:{deck.xp}, kLp:{deck.kLp}, kRp:{deck.kRp}, ADp:{deck.ADp}, kARp:{deck.kARp}, Min.deck Pressure:{deck.PDM_MIN}, deck Pressure_p:{deck.deck_pressure_p}, k2:{deck.k2}, k3:{deck.k3}, kC:{deck.kC}")
        # print(f"\nxs:{deck.xs}, kLs:{deck.kLs}, kRs:{deck.kRs}, ADs:{deck.ADs}, kARs:{deck.kARs}, Min.deck Pressure:{deck.PDM_MIN}, deck Pressure_s:{deck.deck_pressure_s}, kCS:{deck.kCS}")
        print(f"\nEl espesor de las láminas de la cubierta calculado es: {deck.t:.5f} [mm]")
        if craft.material == 'FRP-Sandwich':
            print(f"El Módulo de sección mínimo requerido de la piel exterior para un laminado sándwich de 1 cm de ancho es de: {deck.SM_0} [cm^3/cm], y para el laminado interior es de: {deck.SM_1} [cm^3/cm]")
        print(f"\nEl Area del alma minima es de: {deck.AW:.5f} [cm^2], y el módulo de sección mínimo para los refuerzos de la cubierta es de: {deck.SM:.5f} [cm^3]")
        print(f"Adicionalmente, el Segundo Momento de Inercia mínimo requerido para los refuerzos es de {deck.second_I} [cm^4]") if craft.material in ['FRP-Single Skin', 'FRP-Sandwich'] else None
    else:   #SDBI
        raise ValueError("Material error no reconocido")
        # sdbi = SDBI(craft)
        # Panel_Position  = ['Front','Side (Walking Area)','Side (Non Walking Area)','Aft end','Top <= 800 mm above deck','Top > 800mm above deck','Upper_Tiers']
        # print(f"\ntype:{craft.type}, category:{craft.category}, zone:{craft.zone}, kDC:{craft.kDC}, nCG:{craft.nCG}, material:{craft.material}, esf.diseño_p:{craft.sigma_dp}, esf.diseño_s:{craft.sigma_ds}, esf.diseño_cortante_s:{craft.tau_ds}, kSA:{craft.kSA}")
        # print(f"\nxp:{sdbi.xp}, kLp:{sdbi.kLp}, kRp:{sdbi.kRp}, ADp:{sdbi.ADp}, kARp:{sdbi.kARp}, Min.sdbi Pressure:{sdbi.PDM_MIN}, PDM_Base:{sdbi.PDM_BASE}, PSDS_pressure_p:{sdbi.PSDS_pressure_p}, PWB_p:{sdbi.PWB_p}, PTB_p:{sdbi.PTB_p}, k2:{sdbi.k2}, k3:{sdbi.k3}")
        # print(f"\nxs:{sdbi.xs}, kLs:{sdbi.kLs}, kRs:{sdbi.kRs}, ADs:{sdbi.ADs}, kARs:{sdbi.kARs}, Min.sdbi Pressure:{sdbi.PDM_MIN}, PDM_Base:{sdbi.PDM_BASE}, PSDS_pressure_s:{sdbi.PSDS_pressure_s}, PWB_s:{sdbi.PWB_s}, PTB_s:{sdbi.PTB_s}, kC:{sdbi.kC}")
        # print("\nEl espesor de las láminas calculado es:")
        # for position, thickness in zip(Panel_Position, sdbi.SDBI_thickness):
        #     print(f"{position}: {thickness:.5f} [mm]")
        # print("\nEl módulo de sección mínimo y el área del alma mínima para los refuerzos es de:")
        # for position, sm_value, aw_value in zip(Panel_Position, sdbi.SM_values, sdbi.AW_values):
        #     print(f"{position}: {sm_value:.5f} [cm^3], {aw_value:.5f} [cm^2]")
if __name__ == "__main__":
    main()
