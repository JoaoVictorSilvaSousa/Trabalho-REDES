try:
    bits_input = input("Digite a quantidade de bits da máscara de rede (ex: 24): ")
    bits = int(bits_input)

    if not 0 <= bits <= 32:
        print("Erro: O número de bits deve ser um valor entre 0 e 32.")
    else:
        mascara_binaria = '1' * bits + '0' * (32 - bits)
        octetos_binarios = [mascara_binaria[i:i+8] for i in range(0, 32, 8)]
        octetos_decimais = [int(octeto, 2) for octeto in octetos_binarios]
        mascara_decimal_final = ".".join(map(str, octetos_decimais))
        mascara_binaria_final = ".".join(octetos_binarios)

        print("\n--- Resultados ---")
        print(f"Quantidade de bits: {bits}")
        print(f"A máscara de rede para /{bits} é:")
        print(f"Em formato decimal: {mascara_decimal_final}")
        print(f"Em octetos binários: {mascara_binaria_final}")
except ValueError:
    print("Erro: Por favor, digite um número inteiro válido.")