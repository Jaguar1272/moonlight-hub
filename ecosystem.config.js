module.exports = {
  apps: [
    {
      name: "moonlight-web",
      script: "./venv/bin/uvicorn",
      args: "app.main:app --host 127.0.0.1 --port 8000",
      interpreter: "none",
      env: { NODE_ENV: "production" }
    },
    {
      name: "moonlight-bot",
      script: "./venv/bin/python",
      args: "app/bot.py",
      interpreter: "none",
      env: { NODE_ENV: "production" }
    }
  ]
};