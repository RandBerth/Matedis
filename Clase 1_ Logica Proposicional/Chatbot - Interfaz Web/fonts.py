class fontScheme:
    """Clase que contiene las fuentes de la aplicación
    
    ...
    Atributos:
    -----------
    primary_font : str
        Fuente primaria del sistema de diseño.
    secondary_font : str
        Fuente secundaria del sistema de diseño.
    h1 : str
        Estilos para encabezados H1.
    h2 : str
        Estilos para encabezados H2.
    h3 : str
        Estilos para encabezados H3.
    h4 : str
        Estilos para encabezados H4.
    h5 : str
        Estilos para encabezados H5.
    h6 : str
        Estilos para encabezados H6.
    subtitle1 : str
        Estilos para subtítulos de primer nivel.
    subtitle2 : str
        Estilos para subtítulos de segundo nivel.
    body1 : str
        Estilos para texto del cuerpo principal.
    body2 : str
        Estilos para texto del cuerpo secundario.
    caption : str
        Estilos para subtítulos.
    overline : str
        Estilos para sobrelineas.
    """
    def __init__(self,color_scheme):
        self.primary_font = 'Roboto'
        self.secondary_font = 'serif'
        #home
        self.title = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '2em', 'bold',  '#4B4B4B; ')
        self.tab = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '1em', 'bold', '#00B4D8; ')
        #headers
        self.h1 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '2em', 'bold',  '#333333; ')
        self.h2 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '1.5em', 'bold', 'white; ')
        self.h3 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '1.17em', 'bold', 'white; ')
        self.h4 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '1em', 'bold', 'white; ')
        self.h5 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '0.875em', 'bold', 'white; ')
        self.h6 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '0.75em', 'bold', 'white; ')
        #subtitulos
        self.subtitle1 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '1em', 'medium', 'white; ')
        self.subtitle2 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '0.875em', 'medium', 'white; ')
        #texto del cuerpo
        self.body1 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '1em', 'normal', 'white; ')
        self.body2 = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '0.875em', 'normal', '#333333; ')
        #caption y overline
        self.caption = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '0.75em', 'light', 'white; ')
        self.overline = "font-family: {}; font-size: {}; font-weight: {}; color: {};".format(self.primary_font, '0.625em', 'light', 'white; ')
