from flask import Flask, render_template, request

app = Flask(__name__)

IP_ORIGEM = "192.168.1.100"

def validar_ip(ip_str):
    try:
        octetos = ip_str.split('.')
        if len(octetos) != 4: return False
        for octeto in octetos:
            if not 0 <= int(octeto) <= 255: return False
        return True
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def calculadora():
    contexto = {"ip_origem": IP_ORIGEM}

    if request.method == 'POST':
        try:
            bits_input = request.form.get('bits', '').replace('/', '')
            ip_destino_input = request.form.get('ip_destino', '')

            if not bits_input: raise ValueError("O campo 'Bits da Máscara' é obrigatório.")
            if not ip_destino_input: raise ValueError("O campo 'IP de Destino' é obrigatório.")
            
            # A linha abaixo é a que causa o erro.
            # Se o input for "0.21", int("0.21") falha.
            # O 'except' abaixo vai capturar essa falha.
            bits = int(bits_input)

            if not 0 <= bits <= 32: raise ValueError("O número de bits deve ser um valor entre 0 e 32.")
            if not validar_ip(ip_destino_input): raise ValueError("O IP de destino digitado não é um endereço válido.")

            # --- Cálculos ---
            mascara_binaria_str = '1' * bits + '0' * (32 - bits)
            octetos_binarios = [mascara_binaria_str[i:i+8] for i in range(0, 32, 8)]
            octetos_decimais_mascara = [int(octeto, 2) for octeto in octetos_binarios]
            mascara_decimal_final = ".".join(map(str, octetos_decimais_mascara))

            octetos_origem = [int(o) for o in IP_ORIGEM.split('.')]
            octetos_destino = [int(o) for o in ip_destino_input.split('.')]
            rede_origem = [o & m for o, m in zip(octetos_origem, octetos_decimais_mascara)]
            rede_destino = [o & m for o, m in zip(octetos_destino, octetos_decimais_mascara)]
            
            contexto['status'] = 'sucesso'
            contexto['resultados'] = {
                "bits": bits,
                "ip_destino": ip_destino_input,
                "mascara_decimal": mascara_decimal_final,
                "rede_origem": ".".join(map(str, rede_origem)),
                "rede_destino": ".".join(map(str, rede_destino)),
                "mesma_rede": (rede_origem == rede_destino)
            }
        
        # ***** AQUI ESTÁ A MUDANÇA PRINCIPAL *****
        except ValueError as e:
            contexto['status'] = 'erro'
            # Se a mensagem de erro padrão contém "invalid literal for int",
            # nós mostramos a nossa mensagem personalizada.
            if 'invalid literal for int' in str(e):
                contexto['mensagem_erro'] = "O número de bits da máscara deve ser um número inteiro (sem pontos ou vírgulas)."
            else:
                # Para outros ValueErrors (como "IP inválido"), mostramos a mensagem que já definimos.
                contexto['mensagem_erro'] = str(e)
    
    return render_template('index.html', **contexto)

if __name__ == "__main__":
    app.run(debug=True)