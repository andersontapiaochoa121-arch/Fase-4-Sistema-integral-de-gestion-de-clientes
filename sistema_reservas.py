"""
Sistema de Gestión de Reservas y Servicios Empresariales
=========================================================
Módulo principal que gestiona clientes, servicios y reservas
con manejo robusto de errores y registro de logs.
"""

import sys
import io
from abc import ABC, abstractmethod
from datetime import datetime
import os

# Forzar UTF-8 en la consola de Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ===========================================================
# UTILIDADES
# ===========================================================

LOG_FILE = "error_log.txt"

def registrar_log(error: Exception, contexto: str = "") -> None:
    """
    Registra un error en el archivo de log con timestamp y contexto.

    Args:
        error (Exception): La excepción a registrar.
        contexto (str): Descripción opcional del contexto donde ocurrió el error.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{timestamp}] ERROR"
    if contexto:
        mensaje += f" en {contexto}"
    mensaje += f": {str(error)}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(mensaje)


def limpiar_log() -> None:
    """Limpia el archivo de log al inicio de cada ejecución."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


def separador(titulo: str) -> None:
    """Imprime un separador visual con título para mejor legibilidad."""
    print(f"\n{'-' * 55}")
    print(f"  {titulo}")
    print(f"{'-' * 55}")


# ===========================================================
# MODELO: CLIENTE
# ===========================================================

class Cliente:
    """
    Representa a un cliente del sistema con nombre y correo electrónico.

    Attributes:
        nombre (str): Nombre completo del cliente.
        correo (str): Dirección de correo electrónico válida.
    """

    def __init__(self, nombre: str, correo: str) -> None:
        self._nombre = nombre
        self._correo = self._validar_correo(correo)

    @staticmethod
    def _validar_correo(correo: str) -> str:
        """Valida que el correo tenga formato básico correcto."""
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise ValueError(f"Correo inválido: '{correo}'. Debe contener '@' y un dominio.")
        return correo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo: str) -> None:
        self._correo = self._validar_correo(nuevo_correo)

    # Compatibilidad con interfaz anterior
    def get_nombre(self) -> str:
        return self._nombre

    def get_correo(self) -> str:
        return self._correo

    def set_correo(self, correo: str) -> None:
        self.correo = correo

    def __repr__(self) -> str:
        return f"Cliente(nombre='{self._nombre}', correo='{self._correo}')"

    def __str__(self) -> str:
        return f"{self._nombre} <{self._correo}>"


# ===========================================================
# MODELO: SERVICIOS
# ===========================================================

class Servicio(ABC):
    """
    Clase base abstracta para todos los tipos de servicios ofrecidos.

    Attributes:
        nombre (str): Nombre descriptivo del servicio.
        precio (float): Precio unitario del servicio en COP.
    """

    def __init__(self, nombre: str, precio: float) -> None:
        if precio < 0:
            raise ValueError(f"El precio no puede ser negativo. Recibido: ${precio}")
        self._nombre = nombre
        self._precio = precio

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio(self) -> float:
        return self._precio

    # Compatibilidad con interfaz anterior
    def get_precio(self) -> float:
        return self._precio

    @abstractmethod
    def descripcion(self) -> str:
        """Retorna una descripción detallada del servicio."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nombre='{self._nombre}', precio={self._precio})"


class AsesoriaFinanciera(Servicio):
    """Servicio de asesoría en planificación y gestión financiera."""

    def descripcion(self) -> str:
        return f"[Asesoría Financiera]   {self._nombre} - ${self._precio:,.0f}/hora"


class MentoriaNegocios(Servicio):
    """
    Servicio de mentoría empresarial con duración definida.

    Attributes:
        duracion (int): Duración en horas de cada sesión de mentoría.
    """

    def __init__(self, nombre: str, precio: float, duracion: int) -> None:
        super().__init__(nombre, precio)
        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}h")
        self._duracion = duracion

    @property
    def duracion(self) -> int:
        return self._duracion

    def descripcion(self) -> str:
        return f"[Mentoría de Negocios]  {self._nombre} - {self._duracion}h - ${self._precio:,.0f}/hora"


class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría especializada en áreas técnicas o estratégicas."""

    def descripcion(self) -> str:
        return f"[Asesoría Especializada] {self._nombre} - ${self._precio:,.0f}/hora"


class ReservaSala(Servicio):
    """Servicio de reserva de salas para reuniones o eventos corporativos."""

    def descripcion(self) -> str:
        return f"[Reserva de Sala]       {self._nombre} - ${self._precio:,.0f}/hora"


# ===========================================================
# MODELO: RESERVA
# ===========================================================

class Reserva:
    """
    Representa una reserva de servicio realizada por un cliente.

    Attributes:
        cliente (Cliente): Cliente que realiza la reserva.
        servicio (Servicio): Servicio reservado.
        horas (int): Número de horas solicitadas.
        estado (str): Estado actual: 'pendiente', 'confirmada' o 'cancelada'.
    """

    ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada"}

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: int) -> None:
        if horas <= 0:
            raise ValueError(f"Las horas deben ser mayores a 0. Recibido: {horas}h")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "pendiente"
        self._total: float = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def total(self) -> float:
        return self._total

    def calcular_total(self) -> float:
        """Calcula el costo total de la reserva."""
        return self._servicio.get_precio() * self._horas

    def procesar_reserva(self) -> float:
        """
        Confirma la reserva y calcula el total a pagar.

        Returns:
            float: Total calculado de la reserva.

        Raises:
            RuntimeError: Si la reserva ya fue cancelada.
        """
        if self._estado == "cancelada":
            raise RuntimeError("No se puede confirmar una reserva cancelada.")
        self._total = self.calcular_total()
        self._estado = "confirmada"
        print(
            f"  [OK] Reserva confirmada - Cliente: {self._cliente.get_nombre()}"
            f" | Servicio: {self._servicio.nombre}"
            f" | Horas: {self._horas}h"
            f" | Total: ${self._total:,.0f}"
        )
        return self._total

    def cancelar(self) -> None:
        """Cancela la reserva si aún no ha sido cancelada."""
        if self._estado == "cancelada":
            raise RuntimeError("La reserva ya se encuentra cancelada.")
        self._estado = "cancelada"
        print(f"  [ERROR] Reserva cancelada - Cliente: {self._cliente.get_nombre()}"
              f" | Servicio: {self._servicio.nombre}")

    def get_estado(self) -> str:
        return self._estado

    def __repr__(self) -> str:
        return (f"Reserva(cliente='{self._cliente.get_nombre()}', "
                f"servicio='{self._servicio.nombre}', "
                f"horas={self._horas}, estado='{self._estado}')")


# ===========================================================
# EJECUCIÓN PRINCIPAL
# ===========================================================

def main() -> None:
    """Punto de entrada principal del sistema de reservas."""

    limpiar_log()
    servicios: list[Servicio] = []
    reservas: list[Reserva] = []

    # ── OPERACIÓN 1: Crear cliente válido ────────────────────
    separador("OPERACIÓN 1 - Crear cliente válido")
    try:
        cliente1 = Cliente("Anderson Tapia", "anderson.tapia@gmail.com")
        print(f"  [OK] Cliente registrado: {cliente1}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 1")

    # ── OPERACIÓN 2: Crear cliente con correo inválido ───────
    separador("OPERACIÓN 2 - Cliente con correo inválido")
    try:
        cliente2 = Cliente("María López", "correo_invalido")
        print(f"  Cliente: {cliente2.get_nombre()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 2")

    # ── OPERACIÓN 3: Asesoría financiera válida ──────────────
    separador("OPERACIÓN 3 - Asesoría Financiera válida")
    try:
        servicio1 = AsesoriaFinanciera("Plan de inversión", 50000)
        servicios.append(servicio1)
        print(f"  [OK] {servicio1.descripcion()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 3")

    # ── OPERACIÓN 4: Mentoría de negocios válida ─────────────
    separador("OPERACIÓN 4 - Mentoría de Negocios válida")
    try:
        servicio_extra = MentoriaNegocios("Escalamiento", 80000, 3)
        servicios.append(servicio_extra)
        print(f"  [OK] {servicio_extra.descripcion()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 4")

    # ── OPERACIÓN 5: Mentoría con duración negativa ──────────
    separador("OPERACIÓN 5 - Mentoría con duración inválida")
    try:
        servicio_extra2 = MentoriaNegocios("Marketing", 75000, -1)
        servicios.append(servicio_extra2)
        print(f"  [OK] {servicio_extra2.descripcion()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 5")

    # ── OPERACIÓN 6: Segunda asesoría financiera ─────────────
    separador("OPERACIÓN 6 - Segunda Asesoría Financiera")
    try:
        servicio2 = AsesoriaFinanciera("Optimización fiscal", 60000)
        servicios.append(servicio2)
        print(f"  [OK] {servicio2.descripcion()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 6")

    # ── OPERACIÓN 7: Asesoría especializada ─────────────────
    separador("OPERACIÓN 7 - Asesoría Especializada")
    try:
        servicio3 = AsesoriaEspecializada("Consultoría estratégica", 120000)
        servicios.append(servicio3)
        print(f"  [OK] {servicio3.descripcion()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 7")

    # ── OPERACIÓN 8: Reserva de sala con precio negativo ─────
    separador("OPERACIÓN 8 - Sala con precio negativo")
    try:
        servicio4 = ReservaSala("Sala básica", -5000)
        servicios.append(servicio4)
        print(f"  [OK] {servicio4.descripcion()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 8")

    # ── OPERACIÓN 9: Reserva válida ──────────────────────────
    separador("OPERACIÓN 9 - Reserva válida")
    try:
        reserva1 = Reserva(cliente1, servicio1, 4)
        reservas.append(reserva1)
        reserva1.procesar_reserva()
    except (ValueError, RuntimeError, NameError) as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 9")

    # ── OPERACIÓN 10: Reserva con horas negativas ────────────
    separador("OPERACIÓN 10 - Reserva con horas inválidas")
    try:
        reserva2 = Reserva(cliente1, servicio2, -3)
        reservas.append(reserva2)
        reserva2.procesar_reserva()
    except (ValueError, RuntimeError) as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 10")

    # ── OPERACIÓN 11: Cancelar reserva ──────────────────────
    separador("OPERACIÓN 11 - Cancelar una reserva")
    try:
        reserva3 = Reserva(cliente1, servicio3, 2)
        reservas.append(reserva3)
        reserva3.cancelar()
        print(f"  Estado final: {reserva3.get_estado()}")
    except (ValueError, RuntimeError) as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 11")

    # ── OPERACIÓN 12: Actualizar correo del cliente ──────────
    separador("OPERACIÓN 12 - Actualizar correo del cliente")
    try:
        cliente1.set_correo("anderson.nuevo@empresa.com")
        print(f"  [OK] Correo actualizado: {cliente1.get_correo()}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        registrar_log(e, "Operación 12")

    # ── RESUMEN FINAL ────────────────────────────────────────
    separador("RESUMEN DEL SISTEMA")
    print(f"  Servicios registrados : {len(servicios)}")
    print(f"  Reservas realizadas   : {len(reservas)}")
    total_facturado = sum(r.total for r in reservas if r.get_estado() == "confirmada")
    print(f"  Total facturado       : ${total_facturado:,.0f}")
    print(f"\n{'─' * 55}")
    print("  [OK] Sistema ejecutado correctamente")
    print(f"{'─' * 55}\n")


if __name__ == "__main__":
    main()
