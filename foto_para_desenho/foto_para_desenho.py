import streamlit as st
from time import sleep
import cv2
from PIL import Image, UnidentifiedImageError
import numpy as np

#'''
#Este programa transforma uma foto em desenho utilizando IA
#'''

# Ver como alterar os textos do Widget file_uploader 

def converter(imagem, widget):
    try:
        with st.spinner('Convertendo imagem para desenho, Agurade...'):
            img_pil = Image.open(imagem)
            img = np.array(img_pil)
            # Se a imagem for RGBA (com transparência), converta para RGB
            if img.shape[-1] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            # converte para escala de cinza
            grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            invert_img=cv2.bitwise_not(grey_img)
            # Aplica o filtro de Blur e Inversão
            blur_img=cv2.GaussianBlur(invert_img, (111,111),0)
            invblur_img=cv2.bitwise_not(blur_img)
            # Divid
            desenho=cv2.divide(grey_img,invblur_img, scale=256.0)
            # Mostra imagem
            widget.title('Desenho!')
            widget.image(desenho, channels="GRAY")
    except UnidentifiedImageError:
        st.error('Imagem não suportada! Tente outra!', icon="🚨")
        sleep(2)
        st.stop()
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}", icon="🚨")
        sleep(2)
        st.stop()

st.title('Transformando fotos em desenhos!')
imagem = st.file_uploader('Professor Ricardo Roson - Colégio Litteratus')

col_a, col_b = st.columns(2)

if imagem:
    converter(imagem, col_b)
    col_a.title('Imagem original')
    col_a.image(imagem)
else:
    st.warning('Ainda não temos uma imagem!')
