# Base Datos Referencias para Análisis Clínico

class BaseDatosReferencias:
    def __init__(self):
        self.referencias = self.cargar_referencias()

    def cargar_referencias(self):
        # Cargar datos de referencias clínicas desde una fuente de datos
        # Aquí se puede conectar con una base de datos o un archivo
        referencias = {
            'glucosa': {'min': 70, 'max': 100},
            'colesterol': {'min': 160, 'max': 240},
            'presion_sanguinea': {'min': '120/80', 'max': '130/85'}
        }
        return referencias

    def obtener_referencia(self, analito):
        return self.referencias.get(analito, None)  # Devuelve None si no se encuentra el analito

# Ejemplo de uso
if __name__ == '__main__':
    base_datos = BaseDatosReferencias()
    print(base_datos.obtener_referencia('glucosa'))
    print(base_datos.obtener_referencia('colesterol'))
    print(base_datos.obtener_referencia('presion_sanguinea'))
    