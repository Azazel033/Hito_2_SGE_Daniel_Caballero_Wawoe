import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Toplevel
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Base de Datos - Aplicación")
        self.connection = None
        self.create_login_window()

    def create_login_window(self):
        """Crea la ventana de inicio de sesión."""
        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.login_frame, text="Base de Datos:").grid(row=2, column=0, pady=5)
        self.database_entry = tk.Entry(self.login_frame)
        self.database_entry.grid(row=2, column=1, pady=5)

        tk.Button(self.login_frame, text="Conectar", command=self.connect_to_db).grid(row=3, column=0, columnspan=2, pady=10)

    def connect_to_db(self):
        """Conecta a la base de datos MySQL."""
        user = self.username_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        try:
            self.connection = mysql.connector.connect(
                user=user,
                password=password,
                host="localhost",
                database=database
            )
            if self.connection.is_connected():
                messagebox.showinfo("Éxito", "Conexión establecida con éxito.")
                self.login_frame.destroy()
                self.create_main_window()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo conectar: {err}")

    def create_main_window(self):
        """Crea la ventana principal con filtros y botones."""
        self.main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        # Título
        tk.Label(self.main_frame, text="Consulta de Base de Datos", font=("Arial", 16, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=20)

        # Filtros
        tk.Label(self.main_frame, text="Filtros", font=("Arial", 14, "bold"), bg="#f0f0f0").grid(row=1, column=0, columnspan=2, pady=10)

        # Edad mínima y máxima
        tk.Label(self.main_frame, text="Edad mínima:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=5)
        self.min_age_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.min_age_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self.main_frame, text="Edad máxima:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky="e", pady=5)
        self.max_age_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.max_age_entry.grid(row=3, column=1, pady=5, padx=5)

        # Sexo
        tk.Label(self.main_frame, text="Sexo:", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, sticky="e", pady=5)
        self.gender_combo = ttk.Combobox(self.main_frame, values=["", "Hombre", "Mujer"], font=("Arial", 12))
        self.gender_combo.grid(row=4, column=1, pady=5, padx=5)

        # Otros filtros con Combobox
        self.create_filter("Diversión/Dependencia", 5, "DiversionDependenciaAlcohol", ["", "Sí", "No"])
        self.create_filter("Problemas Digestivos", 6, "ProblemasDigestivos", ["", "Sí", "No"])
        self.create_filter("Tensión Alta", 7, "TensionAlta", ["", "Sí", "No", "No lo sé"])
        self.create_filter("Dolor de Cabeza", 8, "DolorCabeza", ["", "Alguna vez", "A menudo", "Muy a menudo", "Nunca"])

        # Botón para consultar
        tk.Button(self.main_frame, text="Consultar", command=self.fetch_data, font=("Arial", 12), bg="#2196F3", fg="white", relief="raised").grid(row=9, column=0, columnspan=2, pady=15)

        # Ajustar tamaño de la ventana
        self.root.geometry("")  # Ajusta el tamaño de la ventana según el contenido

    def create_filter(self, label_text, row_num, filter_name, options):
        """Método para crear un filtro de combobox con opciones personalizadas"""
        tk.Label(self.main_frame, text=label_text + ":", font=("Arial", 12), bg="#f0f0f0").grid(row=row_num, column=0, sticky="e", pady=5)
        combo = ttk.Combobox(self.main_frame, values=options, font=("Arial", 12))
        combo.grid(row=row_num, column=1, pady=5, padx=5)
        setattr(self, filter_name, combo)

    def fetch_data(self):
        """Consulta los datos con filtros y los muestra en una nueva ventana."""
        min_age = self.min_age_entry.get()
        max_age = self.max_age_entry.get()
        gender = self.gender_combo.get()
        fun_dependency = self.DiversionDependenciaAlcohol.get()
        digestive_issues = self.ProblemasDigestivos.get()
        high_tension = self.TensionAlta.get()
        headache = self.DolorCabeza.get()

        # Construir consulta SQL
        query = """
        SELECT idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, PerdidasControl, DiversionDependenciaAlcohol,
               ProblemasDigestivos, TensionAlta, DolorCabeza
        FROM ENCUESTA
        WHERE 1=1
        """
        filters = []

        if min_age:
            query += " AND edad >= %s"
            filters.append(min_age)
        if max_age:
            query += " AND edad <= %s"
            filters.append(max_age)
        if gender:
            query += " AND Sexo = %s"
            filters.append(gender)
        if fun_dependency:
            query += " AND DiversionDependenciaAlcohol = %s"
            filters.append(fun_dependency)
        if digestive_issues:
            query += " AND ProblemasDigestivos = %s"
            filters.append(digestive_issues)
        if high_tension:
            query += " AND TensionAlta = %s"
            filters.append(high_tension)
        if headache:
            query += " AND DolorCabeza = %s"
            filters.append(headache)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, tuple(filters))
            rows = cursor.fetchall()

            # Crear nueva ventana para mostrar los datos
            self.show_data_window(rows)

            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al ejecutar la consulta: {err}")

    def show_data_window(self, rows):
        """Muestra los resultados de la consulta en una nueva ventana."""
        data_window = Toplevel(self.root)
        data_window.title("Resultados de Consulta")

        # Crear el Treeview para mostrar los datos
        tree = ttk.Treeview(data_window,
                            columns=("ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "PerdidasControl",
                                     "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta",
                                     "DolorCabeza"),
                            show="headings")
        tree.grid(row=0, column=0, padx=10, pady=10)

        # Definir columnas
        columns = {
            "ID": "ID", "Edad": "Edad", "Sexo": "Sexo", "BebidasSemana": "Bebidas Semana",
            "CervezasSemana": "Cervezas Semana",
            "PerdidasControl": "Pérdidas de Control", "DiversionDependenciaAlcohol": "Diversión/Dependencia",
            "ProblemasDigestivos": "Problemas Digestivos", "TensionAlta": "Tensión Alta", "DolorCabeza": "Dolor Cabeza"
        }

        # Asignar función de ordenación en las cabeceras
        for col, text in columns.items():
            tree.heading(col, text=text, command=lambda col=col: self.sort_column(tree, col, rows))
            tree.column(col, width=100, anchor="center")

        for row in rows:
            tree.insert("", "end", values=row)

        # Botones para exportar y generar gráficos
        tk.Button(data_window, text="Exportar", command=lambda: self.export_data(rows), font=("Arial", 12),
                  bg="#FF9800", fg="white", relief="raised").grid(row=1, column=0, pady=10)
        tk.Button(data_window, text="Generar Gráfico", command=lambda: self.create_graph_options(rows),
                  font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised").grid(row=2, column=0, pady=10)

    def sort_column(self, treeview, col, rows):
        """Ordena las filas del Treeview al hacer clic en la cabecera de la columna."""
        # Ordenar los datos según la columna clickeada
        col_index = treeview["columns"].index(col)
        sorted_rows = sorted(rows, key=lambda x: x[col_index])

        # Limpiar los elementos actuales del Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insertar las filas ordenadas de nuevo
        for row in sorted_rows:
            treeview.insert("", "end", values=row)

    def export_data(self, rows):
        """Método para exportar los datos a un archivo Excel."""
        try:
            # Crear un DataFrame de los datos consultados
            df = pd.DataFrame(rows, columns=["ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "PerdidasControl",
                                             "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta",
                                             "DolorCabeza"])

            # Guardar el DataFrame como un archivo Excel
            df.to_excel('datos_exportados.xlsx', index=False, engine='openpyxl')

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Los datos se han exportado correctamente a Excel.")
        except Exception as e:
            # Mostrar error si ocurre algún problema
            messagebox.showerror("Error", f"Error al exportar los datos a Excel: {e}")

    def create_graph_options(self, rows):
        """Abre una ventana para configurar las opciones del gráfico."""
        graph_window = Toplevel(self.root)
        graph_window.title("Opciones de Gráfico")

        # Tipo de gráfico
        tk.Label(graph_window, text="Tipo de Gráfico:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
        graph_type_combo = ttk.Combobox(graph_window, values=["Barras", "Líneas", "Pastel"], font=("Arial", 12))
        graph_type_combo.grid(row=0, column=1, pady=5)

        # Eje X
        tk.Label(graph_window, text="Eje X:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        x_axis_combo = ttk.Combobox(graph_window, values=["Edad", "Sexo", "BebidasSemana"], font=("Arial", 12))
        x_axis_combo.grid(row=1, column=1, pady=5)

        # Eje Y
        tk.Label(graph_window, text="Eje Y:", font=("Arial", 12)).grid(row=2, column=0, pady=5)
        y_axis_combo = ttk.Combobox(graph_window, values=["BebidasSemana", "CervezasSemana", "TensionAlta"], font=("Arial", 12))
        y_axis_combo.grid(row=2, column=1, pady=5)

        # Botón de creación de gráfico
        tk.Button(graph_window, text="Crear Gráfico", command=lambda: self.generate_graph(graph_type_combo.get(), x_axis_combo.get(), y_axis_combo.get(), rows), font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised").grid(row=3, column=0, columnspan=2, pady=10)

    def generate_graph(self, graph_type, x_axis, y_axis, rows):
        """Genera el gráfico basado en las opciones seleccionadas."""
        try:
            # Mapea las columnas a los índices para facilitar el acceso
            column_mapping = {
                "Edad": 1,
                "Sexo": 2,
                "BebidasSemana": 3,
                "CervezasSemana": 4,
                "PerdidasControl": 5,
                "DiversionDependenciaAlcohol": 6,
                "ProblemasDigestivos": 7,
                "TensionAlta": 8,
                "DolorCabeza": 9
            }

            # Obtener los datos del eje X y Y usando los índices
            x_data = [row[column_mapping[x_axis]] for row in rows]
            y_data = [row[column_mapping[y_axis]] for row in rows]

            # Crear gráfico basado en el tipo seleccionado
            plt.figure(figsize=(10, 6))
            if graph_type == "Barras":
                plt.bar(x_data, y_data, color='skyblue')
            elif graph_type == "Líneas":
                plt.plot(x_data, y_data, color='green', marker='o')
            elif graph_type == "Pastel":
                plt.pie(y_data, labels=x_data, autopct='%1.1f%%', startangle=90)

            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            plt.title(f'Gráfico de {x_axis} contra {y_axis}')
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el gráfico: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
