import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Permisos
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Conexión
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Pedidos JB Imports").sheet1

# Generar ID
def generar_id():
    registros = sheet.get_all_values()
    return str(len(registros)).zfill(4)

# Crear pedido
def crear_pedido(cliente, producto, metodo_pago, entrega):
    pedido_id = generar_id()
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")

    sheet.append_row([
        pedido_id,
        cliente,
        producto,
        "Nuevo",
        "Pendiente",
        metodo_pago,
        fecha,
        entrega
    ])

    return pedido_id

# Actualizar estado
def actualizar_estado(pedido_id, estado_pedido=None, estado_pago=None):
    registros = sheet.get_all_values()

    for i, fila in enumerate(registros):
        if fila[0] == pedido_id:
            if estado_pedido:
                sheet.update_cell(i+1, 4, estado_pedido)
            if estado_pago:
                sheet.update_cell(i+1, 5, estado_pago)
            return True

    return False