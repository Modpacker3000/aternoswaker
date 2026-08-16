import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from python_aternos import Client

app = Flask(__name__)

@app.route('/')
@app.route('/ping')
def ping():
    return "Bot activo", 200

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASS = os.getenv("ATERNOS_PASS")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f'Bot encendido como {bot.user}')

@bot.slash_command(name="aternos", description="Prende o apaga el servidor")
async def aternos(
    ctx: discord.ApplicationContext, 
    accion: discord.Option(str, "Selecciona opción", choices=["on", "off"])
):
    await ctx.defer()
    try:
        aternos_api = Client.from_credentials(ATERNOS_USER, ATERNOS_PASS)
        servidores = aternos_api.list_servers()
        if not servidores:
            await ctx.respond("No hay servidores en esta cuenta.")
            return

        srv = servidores[0]
        if accion == "on":
            srv.start()
            await ctx.respond(f"🟢 Encendiendo **{srv.subdomain}**...")
        elif accion == "off":
            srv.stop()
            await ctx.respond(f"🔴 Apagando **{srv.subdomain}**...")

    except Exception as e:
        await ctx.respond(f"❌ Error con Aternos: `{str(e)}`")

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.run(DISCORD_TOKEN)
