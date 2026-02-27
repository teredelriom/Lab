from dataclasses import dataclass
from enum import Enum

class Sexo(Enum):
    MASCULINO = 'masculino'
    FEMENINO = 'femenino'

class CategoriaEdad(Enum):
    INFANTE = 'infante'
    NINO = 'niño'
    ADOLESCENTE = 'adolescente'
    ADULTO = 'adulto'
    ANCIANO = 'anciano'

class EtapaERC(Enum):
    ETAPA_1 = 'Etapa 1'
    ETAPA_2 = 'Etapa 2'
    ETAPA_3 = 'Etapa 3'
    ETAPA_4 = 'Etapa 4'

class EstadoParametro(Enum):
    NORMAL = 'normal'
    ANORMAL = 'anormal'

class SeveridadAnomalias(Enum):
    LEVE = 'leve'
    MODERADO = 'moderado'
    GRAVE = 'grave'

class NivelAlerta(Enum):
    BAJO = 'bajo'
    MEDIO = 'medio'
    ALTO = 'alto'

class TipoReferencia(Enum):
    CLINICO = 'clinico'
    LABORATORIAL = 'laboratorial'

@dataclass
class PerfilPaciente:
    nombre: str
    edad: int
    sexo: Sexo
    categoria_edad: CategoriaEdad

    def to_dict(self):
        return {'nombre': self.nombre, 'edad': self.edad, 'sexo': self.sexo.value, 'categoria_edad': self.categoria_edad.value}

@dataclass
class RangoReferencia:
    minimo: float
    maximo: float
    unidad: str

    def to_dict(self):
        return {'minimo': self.minimo, 'maximo': self.maximo, 'unidad': self.unidad}

@dataclass
class Parametro:
    nombre: str
    rango_referencia: RangoReferencia

    def to_dict(self):
        return {'nombre': self.nombre, 'rango_referencia': self.rango_referencia.to_dict()}

@dataclass
class ResultadoParametro:
    parametro: Parametro
    valor: float
    estado: EstadoParametro

    def to_dict(self):
        return {'parametro': self.parametro.to_dict(), 'valor': self.valor, 'estado': self.estado.value}

@dataclass
class Alerta:
    resultado: ResultadoParametro
    severidad: SeveridadAnomalias
    nivel_alerta: NivelAlerta

    def to_dict(self):
        return {'resultado': self.resultado.to_dict(), 'severidad': self.severidad.value, 'nivel_alerta': self.nivel_alerta.value}

@dataclass
class Examen:
    nombre: str
    resultados: list[ResultadoParametro]

    def to_dict(self):
        return {'nombre': self.nombre, 'resultados': [resultado.to_dict() for resultado in self.resultados]}

@dataclass
class ResultadoAnalisis:
    examen: Examen
    alertas: list[Alerta]

    def to_dict(self):
        return {'examen': self.examen.to_dict(), 'alertas': [alerta.to_dict() for alerta in self.alertas]}