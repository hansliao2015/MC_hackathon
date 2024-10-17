import streamlit as st
import streamlit.components.v1 as components

# if __name__ == "__main__":
#   with open("./html/vehicle.html") as fp:
#     html = fp.read()
#   with open("./js/vehicle.js") as fp:
#     script = fp.read()
#     html = html.replace("SCRIPT", f"<script>{script}</script>")

#   components.html(html, height=700)

def drawPlot():
  with open("./html/vehicle.html") as fp:
    html = fp.read()
  with open("./js/vehicle.js") as fp:
    script = fp.read()
    html = html.replace("SCRIPT", f"<script>{script}</script>")

  components.html(html, height=700)

drawPlot()