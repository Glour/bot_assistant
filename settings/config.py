from environs import Env

env = Env()
env.read_env()

bot_token = env.str("BOT_TOKEN")
openai_api_key = env.str("OPENAI_API_KEY")
