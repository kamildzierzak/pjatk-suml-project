import streamlit as st
import streamlit_authenticator as stauth
import yaml

from database import init_db
from streamlit_authenticator.utilities import LoginError
from yaml.loader import SafeLoader

def main():
  st.set_page_config(
    page_title="Home", 
    page_icon="✨", 
    layout="centered"
  )

  # init_db()

  st.title("🌌 ConstellationRecognizer6001X Deluxe")
  st.write("""
          Zaloguj się, aby uzyskać dostęp do aplikacji.
          Do dyspozycji masz konto testowe:
          - login: test
          - hasło: test
           """)

  with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

  authenticator = stauth.Authenticator(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
  )

  st.session_state["authenticator"] = authenticator
  st.session_state["config"] = config

  try:
    authenticator.login()
  except Exception as e:
    st.error(e)

if __name__ == "__main__":
  main()