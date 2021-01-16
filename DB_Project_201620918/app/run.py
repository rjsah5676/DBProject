from app import app

app.debug=True
app.secret_key = "123"
if __name__ == "__main__":
    app.run()