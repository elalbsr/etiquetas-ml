from pypdf import PdfReader, PdfWriter, PageObject

def combinar_pdf_mercadolibre(archivo_entrada, archivo_salida):
    try:
        reader = PdfReader(archivo_entrada)
        writer = PdfWriter()

        # Verificamos que tenga al menos las 2 páginas (Etiqueta + Detalle)
        if len(reader.pages) >= 2:
            pagina_etiqueta = reader.pages[0]
            pagina_detalle = reader.pages[1]

            # Obtenemos las dimensiones de la página original
            ancho = pagina_etiqueta.mediabox.width
            alto = pagina_etiqueta.mediabox.height

            # Creamos una hoja en blanco con el mismo ancho, pero el doble de alto
            nueva_pagina = PageObject.create_blank_page(width=ancho, height=alto * 2)

            # Pegamos la etiqueta en la mitad superior
            nueva_pagina.merge_translated_page(pagina_etiqueta, tx=0, ty=alto)
            
            # Pegamos el detalle de despacho en la mitad inferior
            nueva_pagina.merge_translated_page(pagina_detalle, tx=0, ty=0)

            # Añadimos la nueva página combinada al escritor
            writer.add_page(nueva_pagina)

            # Guardamos el resultado
            with open(archivo_salida, "wb") as f:
                writer.write(f)
                
            print(f"✅ ¡Éxito! El PDF combinado se guardó como: {archivo_salida}")
        else:
            print("⚠️ El documento no tiene las 2 páginas necesarias.")
            
    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

# --- Ejecución ---
# Cambia los nombres por la ruta real de tus archivos
archivo_original = "44B08E9FF8439989F9DC3C42FC348CE7_labels.pdf"
archivo_final = "Documento_sin_titulo.pdf"

combinar_pdf_mercadolibre(archivo_original, archivo_final)
