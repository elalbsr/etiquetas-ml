import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import io

st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Unificador de Etiquetas Mercado Libre")
st.write("Sube tu etiqueta original. El detalle se ajustará en el espacio en blanco inferior.")

archivo_subido = st.file_uploader("Arrastra tu PDF aquí o haz clic para buscarlo", type="pdf")

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

            # --- PASO 1: Pegar la etiqueta superior ---
            nueva_pagina.merge_page(pagina_etiqueta)

            # --- PASO 2: Ajuste fino de la posición de la Página 2 ---
            # Aquí es donde controlamos qué tan a la derecha y arriba va el comprobante.
            # - Para mover MÁS a la derecha, aumenta el 0.35 (ej: 0.40)
            # - Para mover MÁS hacia arriba, aumenta el 0.08 (ej: 0.12)
            
            desplazamiento_x = ancho * 0.35  
            desplazamiento_y = alto * 0.08   
            
            # Escalar al 50% y aplicar el desplazamiento a la derecha y arriba
            transformacion_p2 = Transformation().scale(0.5, 0.5).translate(desplazamiento_x, desplazamiento_y)
            pagina_detalle.add_transformation(transformacion_p2)
            
            # Pegar el comprobante ya ajustado
            nueva_pagina.merge_page(pagina_detalle)

            writer.add_page(nueva_pagina)

            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)

            st.success("✅ ¡Etiqueta ajustada con las nuevas posiciones!")
            
            st.download_button(
                label="⬇️ Descargar PDF Ajustado",
                data=pdf_bytes,
                file_name="Etiqueta_ML_Lista.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
