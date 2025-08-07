import sqlite3
import csv
from datetime import datetime

DB_NAME = "tareas.db"

def conectar_db():
    """Conecta o crea la base de datos y la tabla de tareas."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tareas
                      (id INTEGER PRIMARY KEY,
                       descripcion TEXT,
                       fecha_vencimiento TEXT,
                       prioridad TEXT,
                       completada INTEGER DEFAULT 0)''')
    conexion.commit()
    return conexion, cursor

def añadir_tarea(cursor, conexion):
    """Permite al usuario añadir una nueva tarea."""
    descripcion = input("Descripción de la tarea: ")
    fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
    prioridad = input("Prioridad (alta/media/baja): ")

    # Aquí debes usar el comando INSERT de SQLite
    cursor.execute("INSERT INTO tareas (descripcion, fecha_vencimiento, prioridad) VALUES (?, ?, ?)", (descripcion, fecha_vencimiento, prioridad))
    conexion.commit()
    print("Tarea añadida con éxito.")

def ver_tareas(cursor):
    """Muestra todas las tareas pendientes y completadas."""
    print("\n--- TAREAS PENDIENTES ---")
    cursor.execute("SELECT id, descripcion, fecha_vencimiento, prioridad FROM tareas WHERE completada = 0")
    for tarea in cursor.fetchall():
        print(f"ID: {tarea[0]} | Descripción: {tarea[1]} | Vence: {tarea[2]} | Prioridad: {tarea[3]}")

    print("\n--- TAREAS COMPLETADAS ---")
    cursor.execute("SELECT id, descripcion, fecha_vencimiento, prioridad FROM tareas WHERE completada = 1")
    for tarea in cursor.fetchall():
        print(f"ID: {tarea[0]} | Descripción: {tarea[1]} | Vence: {tarea[2]} | Prioridad: {tarea[3]}")

def completar_tarea(cursor, conexion):
    """Marca una tarea como completada usando su ID."""
    ver_tareas(cursor)
    tarea_id = input("Introduce el ID de la tarea a completar: ")

    # Aquí debes usar el comando UPDATE de SQLite
    cursor.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (tarea_id,))
    conexion.commit()
    print(f"Tarea con ID {tarea_id} marcada como completada.")

def exportar_csv(cursor):
    """Exporta las tareas pendientes a un archivo CSV."""
    nombre_archivo = "tareas_pendientes.csv"
    cursor.execute("SELECT id, descripcion, fecha_vencimiento, prioridad FROM tareas WHERE completada = 0")

    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(["ID", "Descripción", "Fecha Vencimiento", "Prioridad"])
        escritor_csv.writerows(cursor)

    print(f"Tareas pendientes exportadas a '{nombre_archivo}'.")

def notificar_vencidas(cursor):
    """Bonus: Notifica tareas cuya fecha de vencimiento ha pasado."""
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    print("\n--- NOTIFICACIÓN: TAREAS VENCIDAS ---")
    # Aquí debes usar un SELECT con una cláusula WHERE y la fecha actual
    cursor.execute("SELECT id, descripcion, fecha_vencimiento FROM tareas WHERE completada = 0 AND fecha_vencimiento < ?", (fecha_actual,))

    tareas_vencidas = cursor.fetchall()
    if not tareas_vencidas:
        print("No hay tareas vencidas.")
    else:
        for tarea in tareas_vencidas:
            print(f"¡VENCIDA! ID: {tarea[0]} | Descripción: {tarea[1]} | Venció el: {tarea[2]}")

def menu():
    """Muestra el menú principal y gestiona las opciones del usuario."""
    conexion, cursor = conectar_db()
    notificar_vencidas(cursor) # Llama al bonus al iniciar el programa

    while True:
        print("\n--- GESTOR DE TAREAS ---")
        print("1. Añadir tarea")
        print("2. Ver todas las tareas")
        print("3. Completar tarea")
        print("4. Exportar a CSV")
        print("5. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1':
            añadir_tarea(cursor, conexion)
        elif opcion == '2':
            ver_tareas(cursor)
        elif opcion == '3':
            completar_tarea(cursor, conexion)
        elif opcion == '4':
            exportar_csv(cursor)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, elige un número del 1 al 5.")

    conexion.close()
    print("¡Hasta la próxima!")

if __name__ == "__main__":
    menu()2