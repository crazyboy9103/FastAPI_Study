from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

from routes import example, login, user, auth
app.include_router(example.router)
app.include_router(login.router)
app.include_router(user.router)
app.include_router(auth.router)