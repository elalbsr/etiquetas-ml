import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject
import io

# Configuración de la página web
st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Unificador de Etiquetas Mercado Libre")
st.write("Sube tu etiqueta original de 2 páginas y descarga la versión unificada en una sola hoja para imprimir.")

# Botón para subir el archivo
archivo_subido = st.file_uploader("Arrastra tu PDF aquí o haz clic para buscarlo", type="pdf")

if archivo_subido is not None:
    try:
        reader = PdfReader(archivo_subido)
        writer = PdfWriter()

        # Verificamos que tenga las 2 páginas
        if len(reader.pages) >= 2:
            pagina_etiqueta = reader.pages[0]
            pagina_detalle = reader.pages[1]

            ancho = pagina_etiqueta.mediabox.width
            alto = pagina_etiqueta.mediabox.height

            # Creamos la hoja unificada
            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto * 2)
            nueva_pagina.merge_translated_page(pagina_etiqueta, tx=0, ty=alto)
            nueva_pagina.merge_translated_page(pagina_detalle, tx=0, ty=0)

            writer.add_page(nueva_pagina)

            # Guardamos el resultado en la memoria temporal para permitir la descarga
            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡Etiqueta transformada con éxito!")
            
            # Botón de descarga
            st.download_button(
                label="⬇️ Descargar PDF Unificado",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Lista.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento que subiste no parece tener las 2 páginas necesarias (etiqueta y comprobante).")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")