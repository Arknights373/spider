import sanic

app = sanic.Sanic("Demo")

@app.route("/hello")
async def hello_world(request):
    return sanic.response.text("Hello, world!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)