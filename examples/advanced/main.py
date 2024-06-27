from vortexkit import App
from routes.index import index_route
from middleware import MainMiddleware
from routes.discord_callback import DiscordCallback

app = App()

app.add_route("/", index_route)
app.register_class(
    DiscordCallback()
)

app.register_middleware(
    MainMiddleware()
)

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )