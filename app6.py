import streamlit as st
import requests
from bs4 import BeautifulSoup

@st.cache_data(ttl=60, show_spinner=False)
def obtener_html(url):
    """
    Obtiene el contenido HTML de una URL con un tiempo de vida de caché de 60 segundos.

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
        texto = titulo.get_text(strip=True)
        if texto and len(texto) > 16:
            titulos.append(texto)

    # Buscar títulos en clases específicas comunes en medios
    for elemento in soup.select(".title, .headline, .article-title, .news-title"):
        texto = elemento.get_text(strip=True)
        if texto and texto not in titulos:
            titulos.append(texto)

    return titulos

# Diccionario con medios de comunicación y sus respectivas URL
medios = {
    "Ole": "https://www.ole.com.ar/ultimas-noticias",
    "Clarin deportes": "https://www.clarin.com/deportes",
    "Espn": "https://www.espn.com.ar/",
    "Clarin": "https://www.clarin.com/",
    "La Nacion": "https://www.lanacion.com.ar/",    
    "Infobae": "https://www.infobae.com.ar/",
    "TN": "https://tn.com.ar/",
    "Perfil": "https://www.perfil.com/",    
    "Cronista": "https://www.cronista.com/",
    "Ambito": "https://www.ambito.com/",
}

def main():
    st.title("Scraping de Títulos de Noticias")
    st.write("Este es un ejemplo de scraping de títulos de noticias de varios medios. La caché se actualiza cada 60 segundos.")
    
    for nombre, url in medios.items():
        st.header(f"{nombre} - {url}")
        with st.spinner(f"Scrapeando {nombre}..."):
            html = obtener_html(url)
            titulos = extraer_titulos_noticias(html)
            # Limitar a 30 titulares para cada medio
            titulos = titulos[:30]
        if titulos:
            st.subheader("Títulos de noticias:")
            for titulo in titulos:
                st.write(f"- {titulo}")
        else:
            st.write("No se encontraron títulos de noticias.")

if __name__ == "__main__":
    main()
