import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Etiquetas ML", page_icon="📦")
st.title("📦 Ajuste Perfecto de Etiquetas ML (Modo Imagen)")
st.write("La Hoja 2 se convertirá en imagen para ignorar cualquier margen oculto y encajar perfectamente.")

archivo_subido = st.file_uploader("Arrastra tu PDF aquí", type="pdf")

if archivo_subido is not None:
    try:
        # Leemos el PDF subido en memoria
        pdf_bytes = archivo_subido.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        if len(doc) >= 2:
            st.markdown("---")
            st.subheader("🛠️ Controles de Ajuste")
            
            # Controles interactivos con valores pensados para el cuadrante inferior derecho
            escala = st.slider("1. Tamaño de la Imagen (Escala)", min_value=0.20, max_value=1.00, value=0.45, step=0.01)
            pos_x = st.slider("2. Mover a la Izquierda / Derecha", min_value=0.00, max_value=1.00, value=0.50, step=0.01)
            pos_y = st.slider("3. Mover Abajo / Arriba", min_value=0.00, max_value=1.00, value=0.50, step=0.01)
            
            pagina_etiqueta = doc[0]
            pagina_detalle = doc[1]

            # --- PASO CLAVE: Convertir la Página 2 en una imagen de alta resolución ---
            # dpi=200 asegura que los textos pequeños sigan siendo nítidos al imprimir
            pix = pagina_detalle.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")

            # Obtenemos las dimensiones de la primera hoja
            ancho_p1 = pagina_etiqueta.rect.width
            alto_p1 = pagina_etiqueta.rect.height

            # Calculamos el tamaño final de la imagen basado en tu escala
            img_ancho = ancho_p1 * escala
            img_alto = (pix.height / pix.width) * img_ancho  # Mantiene la proporción original

            # Calculamos las coordenadas (x0, y0) es la esquina superior izquierda de la imagen
            # En PyMuPDF el punto (0,0) está arriba a la izquierda
            x0 = ancho_p1 * pos_x
            y0 = alto_p1 * pos_y
            x1 = x0 + img_ancho
            y1 = y0 + img_alto

            # Definimos el rectángulo donde se pegará la imagen
            rect_destino = fitz.Rect(x0, y0, x1, y1)

            # Insertamos la imagen pura sobre la Página 1
            pagina_etiqueta.insert_image(rect_destino, stream=img_bytes)

            # Creamos un nuevo documento PDF que solo contendrá esta Página 1 modificada
            doc_final = fitz.open()
            doc_final.insert_pdf(doc, from_page=0, to_page=0)

            # Preparamos el archivo para descargar
            pdf_out_bytes = io.BytesIO()
            doc_final.save(pdf_out_bytes)
            doc_final.close()
            doc.close()

            st.success("✅ ¡PDF generado con imagen incrustada! Adiós a los márgenes cortados.")
            
            st.download_button(
                label="⬇️ Descargar PDF Final",
                data=pdf_out_bytes.getvalue(),
                file_name="Etiqueta_ML_Imagen.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El documento no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
