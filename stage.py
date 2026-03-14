#
# # def repeat_text(text: str, n: int) -> str:
# #     result = ""
# #     for i in range(0, n):
# #         result = result + text
# #     return result
# #
# #
# # print(repeat_text("ha", 3))
#
def reverse_number(n: int) -> int:
    text = str(n)[::-1]
    return int(text)


print(reverse_number(1200)) # result: 21