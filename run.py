import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app.bottec_bot.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )