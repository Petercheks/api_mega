#Lector de documento pdf

#### NOTA COLOCAR UN TRY EXCEPT PARA ATRAPAR ERRORES ####

import utilities_pdf_reader as utilities
import pdfplumber
import json


def read(pdf_for_read):
    
    with pdfplumber.open(pdf_for_read) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text(x_tolerance=0, y_tolerance=0)
        lines = text.split('\n')
        
        listCostoEnvio = utilities.getCostosEnvio(lines[26])
        listDivise = utilities.getArrayMontoAprox(lines[30])
        
        data = {
            'fecha_solicitud': lines[0],
            'nro_operacion': utilities.getNroOperation(lines[10]),
            'cajero': utilities.getUserName(lines[3]),
            'solicitante': lines[8].replace(',', ''),
            'tlf_solicitante': utilities.getTlfSolicitante(lines[10]),
            'monto_a_pagar': lines[18].replace('MONTO PAGAR: ', '').strip(),
            'costo_envio': listCostoEnvio[0],
            'total_usd': listCostoEnvio[1],
            'total_pesos': listCostoEnvio[2],
            'tasa_de_cambio': utilities.getTc(lines[30]),
            'divisa': listDivise[0],
            'valor_aprox': listDivise[1].replace(':', ''),
            'oficina_pago': lines[20].replace('OFICINA PAGO: ', ''),
            'transferencia_code': lines[6].replace('SOLICITUD DE TRANSFERENCIA Cod.', ''),
            'beneficiario': lines[14].replace('BENEFICIARIO: ', '').replace(',', ''),
            'tlf_beneficiario': lines[16].replace('TELF: ', '')            
        }
        
        return json.dumps(data, indent=4)
        