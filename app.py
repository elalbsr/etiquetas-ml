import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import io

st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Unificador de Etiquetas Mercado Libre")
st.write("Sube tu etiqueta original y el sistema pondrá el detalle en el espacio en blanco inferior.")

archivo_subido = st.file_uploader("Arrastra tu PDF aquí o haz clic para buscarlo", type="pdf")

if archivo_subido is not None:
    try:
        reader = PdfReader(archivo_subido)
        writer = PdfWriter()

        if len(reader.pages) >= 2:
            pagina_etiqueta = reader.pages[0]
            pagina_detalle = reader.pages[1]

            # Obtenemos las medidas de la hoja base (Página 1)
            ancho = float(pagina_etiqueta.mediabox.width)
            alto = float(pagina_etiqueta.mediabox.height)

            # Creamos la hoja final del MISMO tamaño
            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto)

            # --- PASO 1: Copiar la Página 1 intacta ---
            # Como ya viene en formato "2 en 1", la etiqueta queda perfecta arriba
            nueva_pagina.merge_page(pagina_etiqueta)

            # --- PASO 2: Transformar y pegar la Página 2 ---
            # La Página 2 es individual (muy grande). Para que encaje en el espacio inferior:
            # 1. La achicamos al 50% (0.5) para simular el formato "2 en 1".
            # 2. La centramos horizontalmente (ancho * 0.25).
            # 3. La dejamos en la base (y = 0), por lo que llegará justo hasta la mitad (alto * 0.5).
            transformacion_p2 = Transformation().scale(0.5, 0.5).translate(ancho * 0.25, 0)
            pagina_detalle.add_transformation(transformacion_p2)
            
            # Pegamos la Página 2 ya achicada en el espacio en blanco
            nueva_pagina.merge_page(pagina_detalle)

            writer.add_page(nueva_pagina)

            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡Etiqueta armada con éxito! El detalle se ajustó al espacio en blanco.")
            
            st.download_button(
                label="⬇️ Descargar PDF Final",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Lista.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento que subiste no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
