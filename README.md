# Two Sum (LeetCode) — Solución óptima en Python

**Enunciado:** Dado un arreglo de enteros `nums` y un entero `target`, retorna los **índices** de dos números cuya suma sea `target`.  
**Link del problema:** [https://leetcode.com/problems/two-sum/](https://leetcode.com/problems/two-sum/)

---

## Idea de la solución (óptima)

Se recorre la lista **una sola vez** y se guarda en un diccionario lo que ya se vio:

- `seen[valor] = índice`

En cada posición:
1. Se calcula el **complemento**: `complemento = target - x`
2. Si el complemento ya existe en `seen`, entonces ya tenemos la pareja y devolvemos los índices.

## Ejecución local

Requisitos: **Python 3**

```bash
python two_sum.py
```

---

## Código (two_sum.py)
Incluye la solución y ejemplos simples para validar que funciona:

```python
class Solution:
    # Recorro nums guardando valor -> índice. Para cada x busco si ya vi (target - x).
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}

        for i, x in enumerate(nums):
            complement = target - x
            if complement in seen:
                return [seen[complement], i]
            seen[x] = i

        return []


if __name__ == "__main__":
    s = Solution()

    print(s.twoSum([2, 7, 11, 15], 9))  # [0, 1]
    print(s.twoSum([3, 2, 4], 6))       # [1, 2]
    print(s.twoSum([3, 3], 6))          # [0, 1]
```

---
