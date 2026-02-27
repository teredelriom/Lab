from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Tuple
from datetime import datetime

class Sexo(Enum):
    MASCULINO = "M"
    FEMENINO = "F"
    OTRO = "O"

class CategoriaEdad(Enum):
    RECIEN_NACIDO = "Recién Nacido (0-28 días)"
    LACTANTE = "Lactante (1-12 meses)"
    TODDLER = "Toddler (1-3 años)"
    PREESCOLAR = "Preescolar (3-6 años)"
    ESCOLAR = "Escolar (6-12 años)"
    ADOLESCENTE = "Adolescente (12-18 años)"
    ADULTO_JOVEN = "Adulto Joven (19-35 años)"
    ADULTO = "Adulto (36-59 años)"
    ADULTO_MAYOR = "Adulto Mayor (60-74 años)"
    ANCIANO = "Anciano (≥75 años)"

class EtapaERC(Enum):
    NO_ERC = 0
    ETAPA_1 = 1
    ETAPA_2 = 2
    ETAPA_3a = 3.1
    ETAPA_3b = 3.2
    ETAPA_4 = 4
    ETAPA_5 = 5

class EstadoParametro(Enum):
    BAJO = "Bajo"
    NORMAL = "Normal"
    ALTO = "Alto"
    CRITICO_BAJO = "Críticamente Bajo"
    CRITICO_ALTO = "Críticamente Alto"

class SeveridadAnomalias(Enum):
    LEVE = "Leve"
    MODERADO = "Moderado"
    SEVERO = "Severo"
    CRITICO = "Crítico"

class NivelAlerta(Enum):
    INFO = "ℹ️ INFORMACIÓN"
    ADVERTENCIA = "⚠️ ADVERTENCIA"
    CRÍTICA = "🚨 CRÍTICA"
    URGENCIA = "🔴 URGENCIA CLÍNICA"

class TipoReferencia(Enum):
    LIBRO = "Libro"
    GUIA_CLINICA = "Guía Clínica"
    LABORATORIO = "Laboratorio"
    ARTICULO = "Artículo Científico"
    CONSENSUS = "Consensus/Sociedad"
    PERSONAL = "Personalizado"

@dataclass
class PerfilPaciente:
    edad: int
    sexo: Sexo
    categoria_edad: Optional[CategoriaEdad] = None
    erc_presente: bool = False
    etapa_erc: EtapaERC = EtapaERC.NO_ERC
    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    comorbilidades: List[str] = field(default_factory=list)
    medicamentos: List[str] = field(default_factory=list)
    observaciones: str = ""
    id_paciente: str = field(default_factory=lambda: f"PAC_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    def __post_init__(self):
        self._validar_edad()
        self._determinar_categoria_edad()
    
    def _validar_edad(self):
        if not 0 <= self.edad <= 150:
            raise ValueError(f"Edad inválida: {self.edad}")
    
    def _determinar_categoria_edad(self):
        if self.edad < 1:
            self.categoria_edad = CategoriaEdad.RECIEN_NACIDO
        elif self.edad < 3:
            self.categoria_edad = CategoriaEdad.TODDLER
        elif self.edad < 6:
            self.categoria_edad = CategoriaEdad.PREESCOLAR
        elif self.edad < 12:
            self.categoria_edad = CategoriaEdad.ESCOLAR
        elif self.edad < 18:
            self.categoria_edad = CategoriaEdad.ADOLESCENTE
        elif self.edad < 35:
            self.categoria_edad = CategoriaEdad.ADULTO_JOVEN
        elif self.edad < 60:
            self.categoria_edad = CategoriaEdad.ADULTO
        elif self.edad < 75:
            self.categoria_edad = CategoriaEdad.ADULTO_MAYOR
        else:
            self.categoria_edad = CategoriaEdad.ANCIANO
    
    def calcular_imc(self) -> Optional[float]:
        if self.peso_kg and self.talla_cm:
            talla_m = self.talla_cm / 100
            return round(self.peso_kg / (talla_m ** 2), 1)
        return None
    
    def to_dict(self) -> Dict:
        return {
            "id_paciente": self.id_paciente,
            "edad": self.edad,
            "sexo": self.sexo.value,
            "categoria": self.categoria_edad.value if self.categoria_edad else "N/A",
            "peso_kg": self.peso_kg,
            "talla_cm": self.talla_cm,
            "imc": self.calcular_imc(),
            "erc_presente": self.erc_presente,
            "etapa_erc": self.etapa_erc.value if self.erc_presente else "N/A",
            "comorbilidades": self.comorbilidades,
            "medicamentos": self.medicamentos,
        }

@dataclass
class RangoReferencia:
    minimo: float
    maximo: float
    minimo_critico: Optional[float] = None
    maximo_critico: Optional[float] = None
    categoria_edad: Optional[CategoriaEdad] = None
    sexo: Optional[Sexo] = None
    etapa_erc: Optional[EtapaERC] = None
    imc_rango: Optional[Tuple[float, float]] = None
    fuente_academica: str = "Estándar"
    tipo_referencia: TipoReferencia = TipoReferencia.LIBRO
    fecha_actualizacion: str = field(default_factory=lambda: datetime.now().isoformat())
    notas: str = ""
    
    def contiene(self, valor: float) -> bool:
        return self.minimo <= valor <= self.maximo
    
    def es_critico(self, valor: float) -> bool:
        if self.minimo_critico is not None and valor < self.minimo_critico:
            return True
        if self.maximo_critico is not None and valor > self.maximo_critico:
            return True
        return False
    
    def clasificar_valor(self, valor: float) -> EstadoParametro:
        if self.es_critico(valor):
            return EstadoParametro.CRITICO_BAJO if valor < self.minimo else EstadoParametro.CRITICO_ALTO
        if valor < self.minimo:
            return EstadoParametro.BAJO
        elif valor > self.maximo:
            return EstadoParametro.ALTO
        return EstadoParametro.NORMAL
    
    def to_dict(self) -> Dict:
        return {
            "rango_normal": f"{self.minimo} - {self.maximo}",
            "rango_critico": f"< {self.minimo_critico} / > {self.maximo_critico}" if self.minimo_critico or self.maximo_critico else "N/A",
            "categoria_edad": self.categoria_edad.value if self.categoria_edad else "General",
            "sexo": self.sexo.value if self.sexo else "Ambos",
            "fuente": self.fuente_academica,
            "tipo": self.tipo_referencia.value
        }

@dataclass
class Parametro:
    nombre: str
    abreviaturas: List[str]
    unidad_standar: str
    valores_normales: List[RangoReferencia] = field(default_factory=list)
    descripcion: str = ""
    unidades_alternativas: Dict[str, float] = field(default_factory=dict)
    rango_valores_biologicos: Tuple[float, float] = (0, float('inf'))
    
    def encontrar_abreviatura_coincidente(self, texto: str) -> bool:
        texto_limpio = texto.strip().lower()
        for abr in self.abreviaturas:
            if abr.lower() in texto_limpio or texto_limpio in abr.lower():
                return True
        return False
    
    def validar_biologicamente(self, valor: float) -> Tuple[bool, str]:
        min_bio, max_bio = self.rango_valores_biologicos
        if valor < min_bio or valor > max_bio:
            return False, f"Valor fuera de rango: {min_bio}-{max_bio}"
        return True, "Válido"
    
    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "abreviaturas": self.abreviaturas,
            "unidad": self.unidad_standar,
            "descripcion": self.descripcion,
            "rangos_definidos": len(self.valores_normales)
        }

@dataclass
class ResultadoParametro:
    parametro: Parametro
    valor: float
    unidad: str
    estado: EstadoParametro
    severidad: SeveridadAnomalias
    rango_aplicado: RangoReferencia
    interpretacion: str
    es_critico: bool
    notas_clinicas: str = ""
    flags: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "parametro": self.parametro.nombre,
            "valor": self.valor,
            "unidad": self.unidad,
            "rango": f"{self.rango_aplicado.minimo} - {self.rango_aplicado.maximo}",
            "estado": self.estado.value,
            "severidad": self.severidad.value,
            "interpretacion": self.interpretacion,
            "critico": self.es_critico,
            "flags": self.flags,
            "notas": self.notas_clinicas
        }

@dataclass
class Alerta:
    nivel: NivelAlerta
    parametro: str
    valor: float
    rango_normal: str
    mensaje: str
    recomendacion: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "nivel": self.nivel.value,
            "parametro": self.parametro,
            "valor": self.valor,
            "rango": self.rango_normal,
            "mensaje": self.mensaje,
            "recomendacion": self.recomendacion,
            "timestamp": self.timestamp
        }

@dataclass
class Examen:
    nombre: str
    parametros: List[Parametro] = field(default_factory=list)
    descripcion: str = ""
    version: str = "1.0"
    categoria: str = "General"
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    fuente_principal: str = "Sistema"
    
    def agregar_parametro(self, param: Parametro):
        if not any(p.nombre == param.nombre for p in self.parametros):
            self.parametros.append(param)
    
    def obtener_parametro(self, nombre_o_abr: str) -> Optional[Parametro]:
        texto_limpio = nombre_o_abr.lower().strip()
        for param in self.parametros:
            if param.nombre.lower() == texto_limpio:
                return param
        for param in self.parametros:
            if param.encontrar_abreviatura_coincidente(nombre_o_abr):
                return param
        return None
    
    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "parametros": [p.to_dict() for p in self.parametros],
            "version": self.version,
            "fuente": self.fuente_principal
        }

@dataclass
class ResultadoAnalisis:
    perfil_paciente: PerfilPaciente
    examen_realizado: Examen
    resultados_parametros: List[ResultadoParametro] = field(default_factory=list)
    patrones_detectados: List[str] = field(default_factory=list)
    hipotesis_diagnosticas: List[str] = field(default_factory=list)
    alertas: List[Alerta] = field(default_factory=list)
    recomendaciones_estudio: List[str] = field(default_factory=list)
    calculos_auxiliares: Dict[str, Dict] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    id_analisis: str = field(default_factory=lambda: f"ANL_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    def agregar_resultado(self, resultado: ResultadoParametro):
        self.resultados_parametros.append(resultado)
        if resultado.es_critico:
            alerta = Alerta(
                nivel=NivelAlerta.CRÍTICA,
                parametro=resultado.parametro.nombre,
                valor=resultado.valor,
                rango_normal=f"{resultado.rango_aplicado.minimo}-{resultado.rango_aplicado.maximo}",
                mensaje=f"Valor CRÍTICO en {resultado.parametro.nombre}: {resultado.valor} {resultado.unidad}",
                recomendacion="Revisar inmediatamente"
            )
            self.alertas.append(alerta)
    
    def obtener_resultados_anormales(self) -> List[ResultadoParametro]:
        return [r for r in self.resultados_parametros if r.estado != EstadoParametro.NORMAL]
    
    def obtener_resultados_criticos(self) -> List[ResultadoParametro]:
        return [r for r in self.resultados_parametros 
               if r.estado in [EstadoParametro.CRITICO_ALTO, EstadoParametro.CRITICO_BAJO]]
    
    def to_dict(self) -> Dict:
        return {
            "id_analisis": self.id_analisis,
            "timestamp": self.timestamp,
            "perfil": self.perfil_paciente.to_dict(),
            "examen": self.examen_realizado.nombre,
            "resultados": [r.to_dict() for r in self.resultados_parametros],
            "patrones_detectados": self.patrones_detectados,
            "hipotesis": self.hipotesis_diagnosticas,
            "alertas": [a.to_dict() for a in self.alertas],
            "recomendaciones": self.recomendaciones_estudio,
            "calculos": self.calculos_auxiliares
        }