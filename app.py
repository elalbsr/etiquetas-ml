import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import io

st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Unificador de Etiquetas Mercado Libre")
st.write("Sube tu etiqueta original de 2 páginas y descárgala formateada con ambas en una sola hoja.")

archivo_subido = st.file_uploader("Arrastra tu PDF aquí o haz clic para buscarlo", type="pdf")

if archivo_subido is not None:
    try:
        reader = PdfReader(archivo_subido)
        writer = PdfWriter()

        if len(reader.pages) >= 2:
            pagina_etiqueta = reader.pages[0]
            pagina_detalle = reader.pages[1]

            # Tomamos las dimensiones originales (ej. Carta o A4)
            ancho = float(pagina_etiqueta.mediabox.width)
            alto = float(pagina_etiqueta.mediabox.height)

            # Creamos la hoja final del MISMO tamaño que una hoja normal
            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto)

            # Factor de escala (aprox 70.7%) para que al rotarla quepa en la mitad de la hoja
            escala = ancho / alto

            # --- TRANSFORMACIÓN PÁGINA 1 (Etiqueta principal) ---
            # 1. Achicamos 2. Rotamos -90 grados 3. La subimos a la mitad superior
            transformacion_p1 = Transformation().scale(escala, escala).rotate(-90).translate(0, alto)
            pagina_etiqueta.add_transformation(transformacion_p1)
            nueva_pagina.merge_page(pagina_etiqueta)

            # --- TRANSFORMACIÓN PÁGINA 2 (Detalle del producto) ---
            # 1. Achicamos 2. Rotamos -90 grados 3. La ponemos en la mitad inferior
            transformacion_p2 = Transformation().scale(escala, escala).rotate(-90).translate(0, alto / 2)
            pagina_detalle.add_transformation(transformacion_p2)
            nueva_pagina.merge_page(pagina_detalle)

            # Añadimos la nueva hoja armada al documento final
            writer.add_page(nueva_pagina)

            # Preparamos el archivo para la descarga
            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡Etiqueta unificada perfectamente! (Formato 2 en 1)")
            
            st.download_button(
                label="⬇️ Descargar PDF Listo para Imprimir",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Imprimir.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento que subiste no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
