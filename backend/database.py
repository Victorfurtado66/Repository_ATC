import pyodbc

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=MAQUINA-FURTADO\\SQLEXPRESS;"
    "Database=projetoATC;"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(conn_str)


conexao=pyodbc.connect(conn_str)
print("Conexão bem-sucedida!")