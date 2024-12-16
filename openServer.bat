@echo off

wt -w 0 nt -d "./" uvicorn app.main:app --port 8080 --reload

ngrok http --url=https://next-goshawk-eminent.ngrok-free.app 8080
