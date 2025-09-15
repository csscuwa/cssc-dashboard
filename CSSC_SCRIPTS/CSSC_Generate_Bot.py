from cssc_dash.tools.jwt_tokens import get_bot_token


bot_name = input("bot_name: ")
bot_token = get_bot_token(bot_name=bot_name)
print(bot_token)