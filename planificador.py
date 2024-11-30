import csv
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Proceso:
    """
    Representa un proceso con sus características principales.
    """
    nombre: str
    tiempo_llegada: int
    instrucciones: int
    tiempo_restante: int = None


class SimuladorPlanificacion:
    def __init__(self, archivo_csv: str):
        """
        Inicializa el simulador cargando los procesos desde un archivo CSV.

        :param archivo_csv: Ruta del archivo CSV con los procesos
        """
        self.procesos = self.cargar_procesos(archivo_csv)

    def cargar_procesos(self, archivo_csv: str) -> List[Proceso]:
        """
        Carga los procesos desde un archivo CSV.

        :param archivo_csv: Ruta del archivo CSV
        :return: Lista de procesos
        """
        procesos = []
        with open(archivo_csv, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                nombre, tiempo_llegada, instrucciones = fila
                proceso = Proceso(
                    nombre=nombre,
                    tiempo_llegada=int(tiempo_llegada),
                    instrucciones=int(instrucciones),
                    tiempo_restante=int(instrucciones)
                )
                procesos.append(proceso)
        return sorted(procesos, key=lambda p: p.tiempo_llegada)

    def round_robin(self, quantum: int = 3) -> List[str]:
        """
        Implementa el algoritmo de planificación Round Robin.

        :param quantum: Tiempo de quantum para cada proceso
        :return: Secuencia de ejecución de procesos
        """
        tiempo = 0
        secuencia_ejecucion = []
        cola_listos = []
        procesos_pendientes = self.procesos.copy()

        while procesos_pendientes or cola_listos:
            # Agregar procesos que han llegado a la cola de listos
            while procesos_pendientes and procesos_pendientes[0].tiempo_llegada <= tiempo:
                cola_listos.append(procesos_pendientes.pop(0))

            if not cola_listos:
                tiempo += 1
                continue

            # Seleccionar el primer proceso de la cola
            proceso_actual = cola_listos.pop(0)

            # Ejecutar proceso por quantum o hasta completarse
            ejecucion = min(quantum, proceso_actual.tiempo_restante)
            for _ in range(ejecucion):
                secuencia_ejecucion.append(proceso_actual.nombre)

            proceso_actual.tiempo_restante -= ejecucion
            tiempo += ejecucion

            # Agregar procesos que han llegado mientras se ejecutaba
            while procesos_pendientes and procesos_pendientes[0].tiempo_llegada <= tiempo:
                cola_listos.append(procesos_pendientes.pop(0))

            # Reintegrar el proceso si no ha terminado
            if proceso_actual.tiempo_restante > 0:
                cola_listos.append(proceso_actual)

        return secuencia_ejecucion

    def shortest_process_first(self) -> List[str]:
        """
        Implementa el algoritmo Shortest Process First (SJF No Expropiativo).

        :return: Secuencia de ejecución de procesos
        """
        tiempo = 0
        secuencia_ejecucion = []
        cola_listos = []
        procesos_pendientes = self.procesos.copy()

        while procesos_pendientes or cola_listos:
            # Agregar procesos que han llegado a la cola de listos
            while procesos_pendientes and procesos_pendientes[0].tiempo_llegada <= tiempo:
                cola_listos.append(procesos_pendientes.pop(0))

            if not cola_listos:
                tiempo += 1
                continue

            # Ordenar por instrucciones restantes
            cola_listos.sort(key=lambda p: p.instrucciones)
            proceso_actual = cola_listos.pop(0)

            # Ejecutar proceso completamente
            for _ in range(proceso_actual.tiempo_restante):
                secuencia_ejecucion.append(proceso_actual.nombre)

            tiempo += proceso_actual.tiempo_restante
            proceso_actual.tiempo_restante = 0

            # Agregar procesos que han llegado mientras se ejecutaba
            while procesos_pendientes and procesos_pendientes[0].tiempo_llegada <= tiempo:
                cola_listos.append(procesos_pendientes.pop(0))

        return secuencia_ejecucion


def main():
    # Ruta al archivo CSV (asegúrate de ajustar la ruta según tu estructura de proyecto)
    ruta_archivo = 'archivo.csv'

    # Crear simulador
    simulador = SimuladorPlanificacion(ruta_archivo)

    # Simular Round Robin
    print("Secuencia Round Robin (Quantum = 3):")
    secuencia_rr = simulador.round_robin(quantum=3)
    print(", ".join(secuencia_rr))

    # Reinicializar simulador para Shortest Process First
    simulador = SimuladorPlanificacion(ruta_archivo)

    # Simular Shortest Process First
    print("\nSecuencia Shortest Process First:")
    secuencia_spf = simulador.shortest_process_first()
    print(", ".join(secuencia_spf))



if __name__ == "__main__":
    main()