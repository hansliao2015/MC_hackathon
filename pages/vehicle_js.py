import streamlit as st
import streamlit.components.v1 as components

if __name__ == "__main__":
  with open("./index.html") as fp:
    html = fp.read()
  with open("./scripts/vehicle.js") as fp:
    script = fp.read()
    html = html.replace("SCRIPT", f"<script>{script}</script>")

  components.html(html, height=700)
