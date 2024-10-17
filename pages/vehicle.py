import streamlit as st
import streamlit.components.v1 as components

def drawPlot():
  with open("./html/vehicle-v2.html") as fp:
    html = fp.read()

  components.html(html, height=1000, width=820)

drawPlot()