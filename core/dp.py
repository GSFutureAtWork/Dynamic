import random
import string


def levenshtein_distance_iter(s1, s2):
    """
    Calcula a distância de Levenshtein entre duas strings de forma iterativa (bottom-up).

    Complexidade de tempo: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # remoção
                dp[i][j - 1] + 1,  # inserção
                dp[i - 1][j - 1] + cost,  # substituição
            )
    return dp[m][n]


def levenshtein_distance_rec(s1, s2):
    """
    Calcula a distância de Levenshtein entre duas strings usando recursão e cache manual.

    Complexidade de tempo: O(m * n)
    Complexidade de tempo sem cache: O(3^(m+n))
    """
    cache = {}

    def rec(i, j):
        if (i, j) in cache:
            return cache[(i, j)]
        if i == 0:
            result = j
        elif j == 0:
            result = i
        else:
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            result = min(
                rec(i - 1, j) + 1,  # remoção
                rec(i, j - 1) + 1,  # inserção
                rec(i - 1, j - 1) + cost,  # substituição
            )
        cache[(i, j)] = result
        return result

    return rec(len(s1), len(s2))

def main():
    from utils.measure_time import medir_tempo

    def teste_basico():
        print("--- Teste Básico ---")
        s1 = "Augusto"
        s2 = "Augto"

        # Teste Bottom-Up
        iter_distance, iter_time = medir_tempo(levenshtein_distance_iter, s1, s2)
        print(f"Distância iterativa (Bottom-Up) entre '{s1}' e '{s2}': {iter_distance}")
        print(f"Tempo iterativo: {iter_time} milisegundos\n")

        # Teste Top-Down
        rec_distance, rec_time = medir_tempo(levenshtein_distance_rec, s1, s2)
        print(f"Distância recursiva (Top-Down) entre '{s1}' e '{s2}': {rec_distance}")
        print(f"Tempo recursivo: {rec_time} milisegundos")

        print(f"\nResultados iguais: {iter_distance == rec_distance}")

    def teste_desempenho():
        print("\n--- Teste de Desempenho (100 caracteres) ---")
        random.seed(42)
        s1 = "".join(random.choices(string.ascii_letters, k=100))
        s2 = "".join(random.choices(string.ascii_letters, k=100))

        iter_distance, iter_time = medir_tempo(levenshtein_distance_iter, s1, s2)
        print(
            f"Distância iterativa (Bottom-Up) entre strings de 100 caracteres: {iter_distance}"
        )
        print(f"Tempo iterativo: {iter_time} milisegundos\n")

        rec_distance, rec_time = medir_tempo(levenshtein_distance_rec, s1, s2)
        print(
            f"Distância recursiva (Top-Down) entre strings de 100 caracteres: {rec_distance}"
        )
        print(f"Tempo recursivo: {rec_time} milisegundos")

        print(f"\nResultados iguais: {iter_distance == rec_distance}")

    teste_basico()
    teste_desempenho()


if __name__ == "__main__":
    main()