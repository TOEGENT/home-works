from gigachat import GigaChat
import base64

giga = GigaChat(
   credentials="MDE5OWJjZmEtN2Q4My03N2NkLTlhZTMtMzExYjFhMTA5NTYwOjEwMjFlNmIxLTliMzQtNDk2ZC04YjViLTQ1OTgwZjRjNmU4OQ==",
   verify_ssl_certs=False,
   auto_renew_token=True


)

#response = giga.chat("Привет! Как дела?")

class Player:
   def __init__(self,hp,attack,defence):
      self.hp=hp
      self.attack=attack
      self.defence=defence

