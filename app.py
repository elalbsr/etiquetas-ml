import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import io

st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Ajuste Perfecto de Etiquetas ML")
st.write("Usa los controles para encajar el detalle en el lado derecho sin que se corte.")

archivo_subido = st.file_uploader("Arrastra tu PDF aquí", type="pdf")

if archivo_subido is not None:
    try:
        reader = PdfReader(archivo_subido)
        
        if len(reader.pages) >= 2:
            st.markdown("---")
            st.subheader("🛠️ Controles de Ajuste")
            
            # Valores por defecto reducidos para evitar que choque con el borde derecho
            escala = st.slider("1. Tamaño de la Hoja 2 (Escala)", min_value=0.30, max_value=1.00, value=0.50, step=0.01)
            pos_x = st.slider("2. Mover a la Izquierda / Derecha", min_value=0.00, max_value=1.00, value=0.45, step=0.01)
            pos_y = st.slider("3. Mover Abajo / Arriba", min_value=-0.50, max_value=1.00, value=0.15, step=0.01)
            
            writer = PdfWriter()
            pagina_etiqueta = reader.pages[0]
            pagina_detalle = reader.pages[1]

            # ¡LA SOLUCIÓN AL CORTE! 
            # Esto elimina los márgenes de recorte invisibles de la Hoja 2
            pagina_detalle.cropbox.upper_right = pagina_detalle.mediabox.upper_right
            pagina_detalle.cropbox.lower_left = pagina_detalle.mediabox.lower_left

            ancho = float(pagina_etiqueta.mediabox.width)
            alto = float(pagina_etiqueta.mediabox.height)

            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto)

            # 1. Pegar la primera hoja (Formato base)
            nueva_pagina.merge_page(pagina_etiqueta)

            # 2. Calcular los desplazamientos basados en los sliders
            desplazamiento_x = ancho * pos_x
            desplazamiento_y = alto * pos_y
            
            # 3. Aplicar tamaño y posición a la Hoja 2
            transformacion_p2 = Transformation().scale(escala, escala).translate(desplazamiento_x, desplazamiento_y)
            pagina_detalle.add_transformation(transformacion_p2)
            
            # 4. Pegar la Hoja 2 transformada
            nueva_pagina.merge_page(pagina_detalle)
            writer.add_page(nueva_pagina)

            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡PDF generado! Si notas que aún roza el borde, baja un poco el valor de la Posición X.")
            
            st.download_button(
                label="⬇️ Descargar PDF Ajustado",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Final.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
