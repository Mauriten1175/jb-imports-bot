const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason,
    fetchLatestBaileysVersion
} = require("@whiskeysockets/baileys")

const qrcode = require("qrcode-terminal")
const axios = require("axios")

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState("auth")
    const { version } = await fetchLatestBaileysVersion()

    const sock = makeWASocket({
        version,
        auth: state
    })

    sock.ev.on("creds.update", saveCreds)

    sock.ev.on("connection.update", (update) => {
        const { connection, lastDisconnect, qr } = update

        if (qr) {
            console.log("📲 Escaneá este QR:")
            qrcode.generate(qr, { small: true })
        }

        if (connection === "close") {
            const shouldReconnect =
                lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut

            console.log("❌ Conexión cerrada. Reintentando...", shouldReconnect)

            if (shouldReconnect) {
                startBot()
            }
        }

        if (connection === "open") {
            console.log("✅ BOT CONECTADO A WHATSAPP")
        }
    })

    sock.ev.on("messages.upsert", async ({ messages }) => {
        const msg = messages[0]
        if (!msg.message) return

        const texto =
            msg.message.conversation ||
            msg.message.extendedTextMessage?.text

        const numero = msg.key.remoteJid

        if (!texto) return

        console.log("📩", texto)

        if (texto.toLowerCase() === "hola") {
            await sock.sendMessage(numero, {
                text: "👋 Hola! Soy JB Imports\n\nEscribí:\npedido Juan Producto"
            })
        }

        if (texto.toLowerCase().startsWith("pedido")) {
            const partes = texto.split(" ")

            if (partes.length >= 3) {
                const nombre = partes[1]
                const producto = partes.slice(2).join(" ")

                try {
                    await axios.post("http://localhost:5000/pedido", {
                        nombre,
                        producto
                    })

                   await sock.sendMessage(numero, {
    			text:
			"✅ Pedido registrado con éxito!\n\n" +
			"💳 Métodos de pago:\n\n" +
			"🔹 Transferencia:\n" +
			"Alias: jbimporta2\n" +
			"CBU: 1430001713004893650014\n\n" +
			"🔹 Mercado Pago:\n" +
			"https://link.mercadopago.com.ar/jbimporta2\n\n" +
			"📩 Enviá el comprobante para confirmar tu pedido."
                    })
                } catch (err) {
                    console.log(err)
                }
            }
        }
    })
}

startBot()