import time
import pywhatkit
import bot

print("🤖 Bot de WhatsApp iniciado...")

while True:
    comando = input("Escribí comando: ")

    # Crear pedido
    if comando.startswith("pedido"):
        # formato: pedido|nombre|producto|pago|entrega
        try:
            _, nombre, producto, pago, entrega = comando.split("|")
            pedido_id = bot.crear_pedido(nombre, producto, pago, entrega)

            print(f"✅ Pedido creado: {pedido_id}")

        except:
            print("❌ Error en formato")

    # Marcar pagado
    elif comando.startswith("pagado"):
        _, pedido_id = comando.split("|")
        bot.actualizar_estado(pedido_id, estado_pago="Pagado")
        print("💰 Pago actualizado")

    # Marcar enviado
    elif comando.startswith("enviado"):
        _, pedido_id = comando.split("|")
        bot.actualizar_estado(pedido_id, estado_pedido="Enviado")
        print("🚚 Pedido enviado")

    # Marcar entregado
    elif comando.startswith("entregado"):
        _, pedido_id = comando.split("|")
        bot.actualizar_estado(pedido_id, estado_pedido="Entregado")
        print("✅ Pedido entregado")

    else:
        print("Comando no reconocido")