import os
import streamlit as st
st.set_page_config(layout="wide")
import openai

# Obtener la clave de API de OpenAI desde una variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

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

# Preguntar al usuario sobre el número de lecciones deseadas (máximo: 5)
num_lessons = st.sidebar.slider('Selecciona el número de lecciones:', 1, 5, 3)

# Generar el contenido del curso
if st.sidebar.button('Generar Curso'):
    st.write(f'Generando un curso {course_level.lower()} sobre "{course_topic}" con {num_lessons} lecciones...')

    # Inicializar la lista de lecciones
    lessons = []

    # Generar contenido para cada lección
    for i in range(num_lessons):
        st.write(f'Generando contenido para la lección {i+1}...')

        # Llamada a la API de GPT-3 para generar el contenido de la lección
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f"Lección {i+1}: {course_topic}\nNivel: {course_level}\n\n",
            max_tokens=3750,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Obtener la respuesta generada por GPT-3
        lesson_content = response.choices[0].text.strip()

        # Agregar la lección a la lista
        lessons.append(lesson_content)

        # Mostrar el contenido generado
        st.write(f'Contenido de la lección {i+1}:')
        st.write(lesson_content)

        st.write('---')

    # Mostrar el autor de la aplicación
    st.write('Hecho por Moris Polanco')
