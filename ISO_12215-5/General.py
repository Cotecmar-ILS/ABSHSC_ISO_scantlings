from validations import val_data

class Craft:

    ISO_MATERIALS = ['Acero', 'Aluminio', 'Madera (laminada y plywood)', 'Fibra laminada', 'Fibra con nucleo (Sandwich)']
    #Bulking_material = ['Espuma o fieltro saturado de resina', 'Espuma sintética', 'Plywood', 'Sin material de relleno']
    SKIN_TYPE = ['Fibra de vidrio E con filamentos cortados', 'Fibra de vidrio tejida', 'Fibra tejida de carbono, aramida(kevlar) o híbrida']
    CORE_MATERIAL = ['Madera Balsa', 'Núcleo con elongación al corte en rotura < 35 % (PVC entrecruzado, etc.)', 'Núcleo con elongación al corte en rotura > 35 % (PVC lineal, SAN, etc.)', 'Núcleos tipo panal de abeja (compatibles con aplicaciones marinas)']
    ISO_ZONES = ['Fondo', 'Costados y Espejo', 'Cubierta', 'Superestructura', 'Mamparos estancos', 'Mamparos de tanques integrales', 'Placas anti oleaje', 'Mamparos de colisión']
    CONTEXT = ['Plating', 'Stiffeners']
    
    def __init__(self):
        self.LH, self.LWL, self.BWL, self.BC, self.V, self.mLDC, self.B04 = self.general_attributes()
        self.type = 'Displacement' if (self.V/self.LWL**0.5) < 5 else 'Planning'
        self.category = self.ship_category()
        self.material = self.select_material()
        #self.bulking_material = self.select_bulking_material() if self.material == 'Fibra laminada' else None
        self.skin = self.skin_core_type() if self.material in ['Fibra laminada', 'Fibra con nucleo (Sandwich)'] else None
        self.zone = self.zone_structure()
        self.context = self.select_context()
        
    def display_menu(self, items):
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")
    
    def general_attributes(self):
        LH = 16
        LWL = 15
        BWL = 4.5
        BC = 4
        V = 22
        mLDC = 12
        B04 = 14
        return LH, LWL, BWL, BC, V, mLDC, B04
    
    def ship_category(self):
            return 'A'
        
    
    def select_material(self):
        print("\nSeleccione el material de diseño de su embarcación")
        self.display_menu(self.ISO_MATERIALS)
        choice = val_data("\nIngrese el numero correspondiente: ", False, True, -1, 1, len(self.ISO_MATERIALS))
        return self.ISO_MATERIALS[choice - 1]
    
    def skin_core_type(self) -> str:
        if self.material == 'Fibra laminada':
            print("\nSeleccione el tipo de fibra de diseño")
            self.display_menu(self.SKIN_TYPE)
            choice = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.SKIN_TYPE))
            return self.SKIN_TYPE[choice - 1]
        else: # self.material == 'Fibra con nucleo (Sandwich)'
            print("\nSeleccione el tipo de fibra de diseño de la fibra *exterior*")
            self.display_menu(self.SKIN_TYPE)
            choice1 = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.SKIN_TYPE))
            print("\nSeleccione el tipo de fibra de diseño de la fibra *interior*")
            self.display_menu(self.SKIN_TYPE)
            choice2 = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.SKIN_TYPE))
            print("\nSeleccione el tipo de nucleo del sandwich")
            self.display_menu(self.CORE_MATERIAL)
            choice3 = val_data("\nIngrese el número correspondiente: ", False, True, 0, 1, len(self.CORE_MATERIAL))
            return self.SKIN_TYPE[choice1 - 1], self.SKIN_TYPE[choice2 - 1], self.CORE_MATERIAL[choice3 - 1]
    
    def zone_structure(self):
        print("\nSeleccione la zona o estructura a escantillonar")
        self.display_menu(self.ISO_ZONES)
        choice = val_data("\nIngrese el numero correspondiente: ", False, True, -1, 1, len(self.ISO_ZONES))
        return self.ISO_ZONES[choice - 1]
    
    def select_context(self):
        print("\nSeleccione el tipo escantillonado a calcular")
        self.display_menu(self.CONTEXT)
        choice = val_data("\nIngrese el numero correspondiente: ", False, True, -1, 1, len(self.CONTEXT))
        return self.CONTEXT[choice - 1]
    
    # def effective_plating_of_stiffeners_be(self): # Donde implemento esta funcion?
    #     if self.craft.material == 'Acero':
    #         effective_p = 80 * thickeness
    #     elif self.craft.material == 'Aluminio':
    #         effective_p = 60 * thickness
    #     elif self.craft.material == 'Madera (laminada y plywood)':
    #         effective_p = 15 * thickness
    #     elif self.craft.material == 'Fibra laminada':
    #         effective_p = 20 * thickness
    #     else: #self.craft.material == 'Fibra con nucleo (Sandwich)':
    #         effective_p = 20 * thickness  #t = (t_outer_skin + t_inner_skin)
    #     return effective_p