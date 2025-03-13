from app import app, logger

if __name__ == "__main__":
    logger.info("Starting Fridge Monitoring System")
    app.run(host="0.0.0.0", port=5000, debug=True)
