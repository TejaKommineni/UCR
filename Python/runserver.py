from app import app
if __name__ == "__main__":
    context=(r"E:\UCR\UCR.crt", r"E:\UCR\UCR.key")
    app.run(host="0.0.0.0", port=8443, ssl_context=context, debug=True)
