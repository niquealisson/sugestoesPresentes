import os
import qrcode
from django.shortcuts import render, get_object_or_404
from .models import Presente
from django.conf import settings
import crcmod


class Payload:
    def __init__(self, nome, chavepix, valor, cidade, txtId):
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor.replace(',', '.')
        self.cidade = cidade
        self.txtId = txtId

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.txtId_tam = len(self.txtId)

        self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam:02}{self.chavepix}'
        self.transactionAmount_tam = f'{self.valor_tam:02}{float(self.valor):.2f}'
        self.addDataField_tam = f'05{self.txtId_tam:02}{self.txtId}'
        self.nome_tam = f'{self.nome_tam:02}'
        self.cidade_tam = f'{self.cidade_tam:02}'

        self.payloadFormat = '000201'
        self.merchantAccount = f'26{len(self.merchantAccount_tam):02}{self.merchantAccount_tam}'
        self.merchantCategCode = '52040000'
        self.transactionCurrency = '5303986'
        self.transactionAmount = f'54{self.transactionAmount_tam}'
        self.countryCode = '5802BR'
        self.merchantName = f'59{self.nome_tam:02}{self.nome}'
        self.merchantCity = f'60{self.cidade_tam:02}{self.cidade}'
        self.addDataField = f'62{len(self.addDataField_tam):02}{self.addDataField_tam}'
        self.crc16 = '6304'

    def gerarPayload(self):
        payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'
        crc16 = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
        crc16_code = crc16(payload.encode('utf-8'))
        return f"{payload}{crc16_code:04X}"


# Lista de presentes disponíveis
def lista_presentes(request):
    presentes = Presente.objects.filter(status=True)  # Somente os disponíveis
    return render(request, 'presentes/lista_presentes.html', {'presentes': presentes})


# Confirmação do presente e geração do QR Code
def confirmar_presente(request, presente_id):
    presente = get_object_or_404(Presente, id=presente_id)

    # Informações do pagamento
    chave_pix = "alisson_201083@hotmail.com"  # Chave Pix
    nome_beneficiario = "Nique Alisson Pereira de Souza"  # Nome do beneficiário
    cidade = "Iraquara"  # Cidade
    txt_id = "LOJA01"  # ID da transação

    # Gerar o payload Pix
    payload = Payload(
        nome=nome_beneficiario,
        chavepix=chave_pix,
        valor=f"{presente.valor:.2f}",
        cidade=cidade,
        txtId=txt_id,
    ).gerarPayload()

    # Gerar o QR Code
    qr = qrcode.make(payload)

    # Definir o caminho para salvar o QR Code
    qr_code_path = os.path.join(settings.BASE_DIR, 'static', 'qrcodes', f"{presente.id}_pix.png")
    os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
    qr.save(qr_code_path)

    # Passar o QR Code para o template
    return render(request, 'presentes/confirmar_presente.html', {
        'presente': presente,
        'qr_code': f"qrcodes/{presente.id}_pix.png",
    })
