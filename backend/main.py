from enum import Enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

from tortoise.contrib.fastapi import register_tortoise
app = FastAPI()

try: 
    register_tortoise(
        app, 
        config_file = "config.yaml", 
        generate_schemas=True, # generate schemas (IF NOT EXISTS)
        add_exception_handlers=True,
    )
except Exception as e:
    print(e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import example, login, user
app.include_router(example.router)
app.include_router(login.router)
app.include_router(user.router)


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/")
async def test():
    return {"message": "Good"}