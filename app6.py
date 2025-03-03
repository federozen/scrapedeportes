import streamlit as st
import requests
from bs4 import BeautifulSoup

@st.cache_data(show_spinner=False)
def obtener_html(url):
    """
    Obtiene el contenido HTML de una URL.

    Args:
        url (str): La URL de la página web a descargar.

    Returns:
        str: El contenido HTML de la página, o None si hay un error.
    """
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/91.0.4472.124 Safari/537.36')
        }
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()  # Lanza excepción para errores 4xx o 5xx
        return respuesta.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener la página: {e}")
        return None

def extraer_titulos_noticias(html):
    """
    Extrae los títulos de noticias de una página HTML.

    Args:
        html (str): El contenido HTML de la página.

    Returns:
        list: Lista de títulos de noticias encontrados.
    """
    if html is None:
        return []
    soup = BeautifulSoup(html, "html.parser")
    titulos = []

    # Buscar títulos en etiquetas h1, h2, h3
    for titulo in soup.find_all(["h1", "h2", "h3"]):
        texto = titulo.text.strip()
        if texto and len(texto) > 16:
            titulos.append(texto)

    # Buscar títulos en clases específicas comunes en medios
    for elemento in soup.select(".title, .headline, .article-title, .news-title"):
        texto = elemento.text.strip()
        if texto and texto not in titulos:
            titulos.append(texto)

    return titulos

# Diccionario con medios de comunicación y sus respectivas URL
medios = {
    "Ole": "https://www.ole.com.ar",
    "Clarin": "https://www.clarin.com/deportes",    
    "TyC": "https://www.tycsports.com/",
    "dobleamarilla": "https://www.dobleamarilla.com.ar",
    "Espn": "https://www.espn.com.ar/",
    "Infobae": "https://www.infobae.com/deportes/",
    "TN": "https://tn.com.ar/deportes/"
}

def main():
    st.title("Scraping de Títulos de Noticias")
    st.write("Este es un ejemplo de scraping de títulos de noticias de varios medios.")
    
    for nombre, url in medios.items():
        st.header(f"{nombre} - {url}")
        with st.spinner(f"Scrapeando {nombre}..."):
            html = obtener_html(url)
            titulos = extraer_titulos_noticias(html)
            # Limitar a 20 títulos si se trata de dobleamarilla.com
            if "dobleamarilla" in url:
                titulos = titulos[:20]
            if "ole.com" in url:
                titulos = titulos[:30]
            if "tycsports" in url:
                titulos = titulos[:20]                          
        if titulos:
            st.subheader("Títulos de noticias:")
            for titulo in titulos:
                st.write(f"- {titulo}")
        else:
            st.write("No se encontraron títulos de noticias.")

if __name__ == "__main__":
    main()
