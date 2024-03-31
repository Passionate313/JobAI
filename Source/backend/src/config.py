from dotenv import dotenv_values

# set config with values in env
config = dotenv_values(".env")

# mongodb
ATLAS_URI = config["ATLAS_URI"]
DB_NAME = config["DB_NAME"]

# eden ai api key
EDEN_AI_API_KEY = config["EDEN_AI_API_KEY"]

# api layer key
API_LAYER_KEY = config["API_LAYER_KEY"]

# openai
OPENAI_API_KEY = config["OPENAI_API_KEY"]
