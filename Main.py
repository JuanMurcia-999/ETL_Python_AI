from Funtions import extract_text_from_pdf, get_detail_AI, csv_to_dataframe 
import os
from sqlalchemy import create_engine
from time import sleep

folder_path ='./Facturas'
invoice_text = []


# Lectura de los ubicaciones de las facturas
for invoice in sorted(os.listdir(folder_path)):
    route_pdf = os.path.join(folder_path+'/',invoice)

    # Extraccion y guardao de los textos en cada factura
    invoice_text.append(extract_text_from_pdf(route_pdf))
    sleep(0.5)
    print(invoice)

print(len(invoice_text))

# Formateo de datos por parte de la IA
details_from_ai = get_detail_AI(invoice_text)

# Convertir en Dataframe
df = csv_to_dataframe(details_from_ai)


engine = create_engine("sqlite:///facturas.db")
df.to_sql("facturas", engine, if_exists='append', index=False)
engine.dispose()


print('Carga finalizada')