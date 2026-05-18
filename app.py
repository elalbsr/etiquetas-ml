import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import io

# Configuración de la página web
st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Unificador de Etiquetas Mercado Libre")
st.write("Sube tu etiqueta original de 2 páginas y descarga la versión unificada en una sola hoja tamaño estándar.")

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

            # Tomamos las dimensiones de la hoja original (ej. tamaño Carta o A4)
            ancho = float(pagina_etiqueta.mediabox.width)
            alto = float(pagina_etiqueta.mediabox.height)

            # NUEVO: Creamos una hoja con el MISMO tamaño que la original, no el doble
            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto)

            # 1. Pegamos la etiqueta (Página 1). ML siempre la pone en la mitad superior.
            nueva_pagina.merge_page(pagina_etiqueta)

            # 2. Desplazamos la segunda página (detalle) hacia abajo.
            # Le restamos exactamente la mitad del alto de la página para que encaje 
            # perfecto en el espacio en blanco inferior.
            desplazamiento = Transformation().translate(0, -(alto / 2))
            pagina_detalle.add_transformation(desplazamiento)
            
            # Pegamos la segunda página ya desplazada
            nueva_pagina.merge_page(pagina_detalle)

            writer.add_page(nueva_pagina)

            # Guardamos el resultado en la memoria temporal
            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡Etiqueta unificada correctamente en una sola hoja normal!")
            
            # Botón de descarga
            st.download_button(
                label="⬇️ Descargar PDF Unificado",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Lista.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento que subiste no parece tener las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
