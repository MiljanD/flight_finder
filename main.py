from token_manager import TokenManager
import requests


token = TokenManager()
valid_token = token.get_valid_token()

print(valid_token)





