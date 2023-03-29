import yaml
TORTOISE_ORM = yaml.load(open("./config.yaml", "r"), Loader=yaml.FullLoader)