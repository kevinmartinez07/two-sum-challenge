# Recorro la lista y voy guardando (valor -> índice).
# Para cada valor calculo target - valor y reviso si ya lo tengo guardado.
# Cuando aparece, retorno el índice guardado y el actual.
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen: dict[int, int] = {}

        for i, x in enumerate(nums):
            complement = target - x
            if complement in seen:
                return [seen[complement], i]
            seen[x] = i
        return []
        

if __name__ == "__main__":
    s = Solution()

    nums = [2, 7, 11, 15]
    target = 9
    print(s.twoSum(nums, target))  # [0, 1]

    nums = [3, 2, 4]
    target = 6
    print(s.twoSum(nums, target))  # [1, 2]
    
    nums = [3,3]
    target = 6
    print(s.twoSum(nums, target)) # [0, 1]