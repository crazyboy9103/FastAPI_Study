from enum import Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

app = FastAPI()
try: 
    register_tortoise(
        app, 
        config_file = "config.yaml", 
        generate_schemas=True, # generate schemas (IF NOT EXISTS)
        add_exception_handlers=True,
    )
    print(dir(app))
    for model_name, model_class in Tortoise.apps.models.items():
        file_name = f"{model_name.lower()}.py"
        with open(file_name, "w") as f:
            f.write(model_class.__module__ + "\n\n")
            f.write(model_class.__qualname__ + " = ...\n")
            f.write(model_class.__name__ + " = ...\n")
            f.write(str(model_class).replace(model_class.__module__ + ".", ""))

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