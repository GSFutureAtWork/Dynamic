import time

def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fim = time.perf_counter()
    tempo_ms = (fim - inicio) * 1000
    tempo_formatado = f"{tempo_ms:.2f}".replace(".", ",")
    return resultado, tempo_formatado
