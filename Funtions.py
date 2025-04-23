import fitz
from prompt import prompt
from openai import OpenAI
import pandas as pd
from io import StringIO



client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")




def get_detail_AI (text):
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        messages=[
            {"role": "system", "content": "Eres un experto en extracción de datos de facturas. Devuelve solo el CSV sin explicaciones ni mensajes adicionales. Si no puedes extraer datos, devuelve exactamente la palabra 'error' sin comillas."},
            {"role": "user", "content":  prompt + "\n Este es el texto a parsear:\n" + str(text)}],
        stream=False
    )

    return response.choices[0].message.content



def extract_text_from_pdf(pdf_path):
    """Extrae el texto de un archivo PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"

    
    return text




def csv_to_dataframe(csv):

    dtype_cols = {
        "fecha_factura": str,
        "proveedor": str,
        "concepto": str,
        "importe": str,  # Se leerá primero como str para poder limpiar comas
        "moneda": str,
        "cantidad":str,
        "factura":str
    }

    df_temp = pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols)

    # Convertir 'importe' a float, asegurando que los valores con coma se conviertan correctamente
    df_temp["importe"] = pd.to_numeric(
        df_temp["importe"].str.replace(",", "."), errors="coerce"
    )
    
    return df_temp



