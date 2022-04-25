from fastapi import FastAPI


def start_app_handler(app: FastAPI):
    def startup() -> None:
        print("Running app start handler.")
    return startup


def stop_app_handler(app: FastAPI):
    def shutdown() -> None:
        print("Running app shutdown handler.")
    return shutdown