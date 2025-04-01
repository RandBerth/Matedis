class colorScheme:
    """
    Esquema para representar los colores del sistema
    
    '''
    Atributos:
    primary : str
        color primario del diseño del sistema.
    secondary : str
        color secundario del diseño del sistema.
    success : str
        color para acciones exitosas o notificaciones.
    info : str
        color para mensajes informativos.
    warning : str
        color para advertencias.
    danger : str
        color para errores o acciones peligrosas.
    background : str
        color de fondo del diseño del sistema.
    text : str
        color de texto predeterminado.
    Metodos:
    -----
    get_color(name):
        Devuelve el valor del color del esquema por su nombre
    """
    def __init__(self, ui):
        """Construye los elementos necesarios para los colores de los objetos."""
        self.primary =  "#003366"
        self.secondary = "#555555"
        self.success = "#4CAF50"
        self.danger = "#F44336"
        self.warning = "#FFC107"
        self.background = "#ffffff"
        self.text = "#000000"
        self.color_box = "#00B4D8"
        self.color_border = "#FFC107"
        ui.colors(primary=self.primary)
        ui.colors(secondary=self.secondary)

    def get_color(self, name):
        """
        Devuelve el valor del color del esquema por su nombre
        Args:
            name (str): El nombre del color (por ejemplo, 'primary', 'success', etc.)

        Raises:
            ValueError: No se encontró el color con el nombre especificado

        Returns:
            str: El valor del color.
        """
        try:
            return getattr(self, name)
        except AttributeError as e:
            raise ValueError(f"Color {name} no fue encontrado") from e
