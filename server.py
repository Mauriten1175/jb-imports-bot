from flask import Flask, request
import bot

app = Flask(__name__)

@app.route("/pedido", methods=["POST"])
def pedido():
    data = request.json

    nombre = data["nombre"]
    producto = data["producto"]

    bot.crear_pedido(nombre, producto, "Pendiente", "Envio")

    print(f"Pedido creado: {nombre} - {producto}")

    return {"status": "ok"}

app.run(port=5000)