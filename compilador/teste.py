import os
import subprocess

pasta_testes = "./../testes"

arquivos = os.listdir(pasta_testes)

arquivos_java = [arquivo for arquivo in arquivos if arquivo.endswith(".java")]

for arquivo in arquivos_java:
    caminho_arquivo = os.path.join(pasta_testes, arquivo)
    comando = ["python", "sintatico.py", caminho_arquivo]
    
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    print(f"Executando para {arquivo}:")
    print(resultado.stdout)
    print(resultado.stderr)
