import os
import streamlit as st
st.set_page_config(layout="wide")
import openai
import requests
from bs4 import BeautifulSoup

# Obtener la clave de API de OpenAI desde una variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Función para realizar web scraping y obtener enlaces relevantes
def get_relevant_links(query, num_links=5):
    # Realizar una búsqueda en Google
    search_url = f'https://www.google.com/search?q={query}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer los enlaces de los resultados de búsqueda
    links = []
    search_results = soup.select('.kCrYT a')
    for result in search_results:
        link = result.get('href')
        if link.startswith('/url?q='):
            link = link[7:]  # Eliminar el prefijo '/url?q='
            links.append(link)

        if len(links) == num_links:
            break

    return links

# Título de la aplicación
st.title('Generador de Cursos Personalizados')

# Explicación sobre lo que hace la aplicación
st.sidebar.write('Esta aplicación genera cursos personalizados sobre diferentes temas de economía.')

# Temas disponibles para el curso
topics = [
    'La Escuela Austriaca de Economía',
    'La Acción Humana, según Ludwig von Mises',
    'El emprendimiento, según Israel Kirzner',
    'Fundamentos de la moral, según Henry Hazlitt',
    'Teoría de los ciclos económicos, según la Escuela Austriaca',
    'Economía de libre mercado',
    'El liberalismo, según Ludwig von Mises',
    'Teorías del valor económico',
    'Teoría de los sentimientos morales, de Adam Smith',
    'Teoría de la utilidad marginal',
    'La ética del capitalismo',
    'La ley, según Bastiat',
    'El orden espontáneo',
    'La dispersión del conocimiento, según Hayek',
    'El papel del gobierno en una economía libre',
    'El principio de subsidiariedad'
]

# Preguntar al usuario sobre el tema del curso
course_topic = st.sidebar.selectbox('Selecciona un tema:', topics, key='topic')

# Opción para escribir el nombre del curso
custom_topic = st.sidebar.text_input('O ingresa el nombre del curso manualmente:')

# Combinar el tema seleccionado y el tema personalizado
if custom_topic:
    course_topic = custom_topic

# Preguntar al usuario sobre el nivel del curso
course_level = st.sidebar.selectbox('Selecciona el nivel del curso:', ['Principiante', 'Intermedio', 'Avanzado'], key='level')

# Generar el contenido del curso
if st.sidebar.button('Generar Curso'):
    st.write(f'Generando un curso {course_level.lower()} sobre "{course_topic}"...')

    # Llamada a la API de GPT-3 para generar el contenido del curso
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Curso sobre {course_topic}\n\nNivel: {course_level}\n\n",
        max_tokens=2500,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Obtener la respuesta generada por GPT-3
    course_content = response.choices[0].text.strip()

    # Mostrar el contenido generado
    st.write('Contenido del curso:')
    st.write(course_content)

    # Generar y mostrar enlaces web relacionados (máximo: 5)
    st.write('Enlaces web relacionados:')
    links = get_relevant_links(course_topic, num_links=5)
    for link in links:
        st.write(link)

    # Mostrar información adicional del curso
    st.write('Información del curso:')
    st.write('- Descripción:')
    st.write('- Objetivo:')
    st.write('- Duración:')
    st.write('- Lista de contenidos:')

    # Mostrar el autor de la aplicación
    st.write('Hecho por Moris Polanco')
