# def count_unique_lines(filename):
#     unique_lines = set()
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             unique_lines.add(line.strip())  # Удаление пробельных символов с обеих сторон строки
#     return len(unique_lines)
#
# # Путь к файлу, который вы хотите проверить
# filename = 'data/raw_data.txt'
# print(f"Количество уникальных строк в файле: {count_unique_lines(filename)}")
# def remove_duplicate_lines(filename):
#     unique_lines = set()
#     # Чтение файла и сохранение уникальных строк
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             unique_lines.add(line)
#
#     # Перезапись файла уникальными строками
#     with open(filename, 'w', encoding='utf-8') as file:
#         for line in unique_lines:
#             file.write(line)

# # Путь к файлу, из которого нужно удалить дубликаты строк
# filename = 'data/data.txt'
# remove_duplicate_lines(filename)
# print("Дублирующиеся строки удалены.")
#
#
# def split_list_into_four_parts(lst):
#     n = len(lst)
#     part_size = n // 4
#
#     parts = [lst[i * part_size:(i + 1) * part_size] for i in range(4)]
#
#     remainder = n % 4
#     for i in range(remainder):
#         parts[i].append(lst[part_size * 4 + i])
#
#     return parts



