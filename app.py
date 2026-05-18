import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import io

st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Unificador de Etiquetas Mercado Libre")
st.write("El detalle del producto se deslizará intacto hacia la mitad inferior.")

archivo_subido = st.file_uploader("Arrastra tu PDF aquí", type="pdf")

if archivo_subido is not None:
    try:
        reader = PdfReader(archivo_subido)
        writer = PdfWriter()

        if len(reader.pages) >= 2:
            pagina_etiqueta = reader.pages[0]
            pagina_detalle = reader.pages[1]

            ancho = float(pagina_etiqueta.mediabox.width)
            alto = float(pagina_etiqueta.mediabox.height)

            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto)

            # --- PASO 1: Pegar la etiqueta en la mitad superior ---
            nueva_pagina.merge_page(pagina_etiqueta)

            # --- PASO 2: Deslizar la Hoja 2 hacia abajo ---
            # No la achicamos, solo la empujamos hacia abajo en negativo.
            # Multiplicamos el alto por 0.48 (la empuja casi hasta la mitad de la hoja).
            
            desplazamiento_x = 0  # 0 la mantiene centrada igual que la original
            desplazamiento_y = -(alto * 0.48) # El signo negativo la mueve hacia ABAJO
            
            # Aplicamos solo la traslación (sin el .scale que cortaba el PDF)
            transformacion_p2 = Transformation().translate(desplazamiento_x, desplazamiento_y)
            pagina_detalle.add_transformation(transformacion_p2)
            
            # Pegamos el detalle en la nueva página
            nueva_pagina.merge_page(pagina_detalle)

            writer.add_page(nueva_pagina)

            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡Etiqueta generada sin recortes y a tamaño completo!")
            
            st.download_button(
                label="⬇️ Descargar PDF Final",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Lista.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
