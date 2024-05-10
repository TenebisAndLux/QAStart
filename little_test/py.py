for i in range(3):
    print(f"Внешний цикл: {i}")
    for j in range(1000):
        print(f"Внутренний цикл: {j}")
        if j == 1:
            break  # Прерываем только внутренний цикл

print("Программа завершена.")
