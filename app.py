# Este é o endereço IP do nosso computador de origem.
IP_ORIGEM = "192.168.1.100"

def validar_ip(ip_str):
    
    #Função auxiliar para validar se uma string é um endereço IP v4 válido, retorna True se for válido, False caso contrário.
   
    try:
        # Tenta dividir a string em 4 partes usando o ponto como delimitador.
        octetos = ip_str.split('.')
        if len(octetos) != 4:
            return False
        # Verifica se cada parte é um número entre 0 e 255.
        for octeto in octetos:
            if not 0 <= int(octeto) <= 255:
                return False
        return True
    except (ValueError, AttributeError):
        # Se a conversão para inteiro falhar ou a string for inválida.
        return False

def main():
    #Função principal que executa o programa.
    print("--- Calculadora de Rede IP ---")
    print(f"O IP de origem fixo é: {IP_ORIGEM}\n")

    try:
        # 2) Recebe do usuário a máscara de rede em bits.
        bits_input = input("Digite a quantidade de bits da máscara de rede (ex: /24): ").replace('/', '')
        bits = int(bits_input)

        # Valida se o número de bits está no intervalo correto (0 a 32).
        if not 0 <= bits <= 32:
            print("\nErro: O número de bits deve ser um valor entre 0 e 32.")
            return

        # --- Cálculo da Máscara de Rede ---
        # Cria a string binária da máscara (ex: 24 bits '1' seguidos de 8 bits '0').
        mascara_binaria_str = '1' * bits + '0' * (32 - bits)
        
        # Divide a string binária em 4 octetos (grupos de 8 bits).
        octetos_binarios = [mascara_binaria_str[i:i+8] for i in range(0, 32, 8)]
        
        # Converte cada octeto binário para seu valor decimal.
        octetos_decimais_mascara = [int(octeto, 2) for octeto in octetos_binarios]

        # Junta os octetos para formar os endereços de máscara final.
        mascara_decimal_final = ".".join(map(str, octetos_decimais_mascara))
        mascara_binaria_final = ".".join(octetos_binarios)

        print("\n--- Máscara de Rede ---")
        print(f"Máscara para /{bits}:")
        print(f"Em formato decimal: {mascara_decimal_final}")
        print(f"Em octetos binários: {mascara_binaria_final}")

        #Recebe do usuário um IP de destino.
        ip_destino_input = input("\nDigite o IP de destino (ex: 192.168.1.200): ")

        if not validar_ip(ip_destino_input):
            print("\nErro: O IP de destino digitado não é um endereço válido.")
            return

        # --- Verificação de Rede ---
        # Converte os IPs de string para listas de inteiros (octetos).
        octetos_origem = [int(o) for o in IP_ORIGEM.split('.')]
        octetos_destino = [int(o) for o in ip_destino_input.split('.')]

        # Calcula o endereço de rede da origem fazendo a operação E (AND) bit a bit.
        # (IP_ORIGEM & MÁSCARA)
        rede_origem = []
        for i in range(4):
            rede_origem.append(octetos_origem[i] & octetos_decimais_mascara[i])

        # Calcula o endereço de rede do destino.
        # (IP_DESTINO & MÁSCARA)
        rede_destino = []
        for i in range(4):
            rede_destino.append(octetos_destino[i] & octetos_decimais_mascara[i])
        
        # Formata os endereços de rede para exibição.
        rede_origem_str = ".".join(map(str, rede_origem))
        rede_destino_str = ".".join(map(str, rede_destino))

        print("\n--- Análise de Rede ---")
        print(f"Endereço de rede da Origem ({IP_ORIGEM}): {rede_origem_str}")
        print(f"Endereço de rede do Destino ({ip_destino_input}): {rede_destino_str}")
        
        # Compara se os endereços de rede calculados são iguais.
        if rede_origem == rede_destino:
            print("\nConclusão: O IP de destino ESTÁ na mesma rede da origem.")
        else:
            print("\nConclusão: O IP de destino NÃO ESTÁ na mesma rede da origem.")

    except ValueError:
        print("\nErro: Por favor, digite um número inteiro válido para os bits da máscara.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

# Executa a função principal quando o script é iniciado.
if __name__ == "__main__":
    main()