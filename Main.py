import math
import random

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ ,."


def generate_Keys():
    if is_Prime(p) and is_Prime(q):
        if p == q:
            print("Значения p и q не могут быть оиднаковыми")
            exit()
    else:
        print("p и q должны быть простыми числами")
        exit()

    N = p * q
    print("Произведение p и q: N =", N)
    phi = (p - 1) * (q - 1)
    print("Функция Эйлера: phi =", phi)

    e = None
    d = None

    while e is None or e == phi or not is_Prime(e) or d is None:
        e = random.randint(1, phi)
        if math.gcd(e, phi) == 1:
            d = inverse(e, phi)
            if d is not None:
                break

    print("Экспонента: e =", e)
    print("Вычислим D: d =", d)

    return (e, N), (d, N)


def is_Prime(number):
    if number <= 1:
        return False
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    def count_divisors(number):
        count = 0
        sqrt = int(math.sqrt(number))

        for i in range(1, sqrt + 1):
            if number % i == 0:
                count += 1

                if i != number // i:
                    count += 1
                if count > 2:
                    return False
        return True

    return count_divisors(number)


def inverse(e, phi):
    m0, x0, x1 = phi, 0, 1

    while e > 1:
        q = e // phi
        phi, e = e % phi, phi

        x0, x1 = x1 - q * x0, x0

    if e == 1:
        return x1 % m0
    else:
        return None


def rand_Pair(number):
    mid = number // 2

    for num1 in range(mid, 1, -1):
        num2 = number - num1
        if math.gcd(num1, num2) == 1:
            return num1, num2

    return None


def find_Index(message):
    message_index = []
    for char in message:
        if char in alphabet:
            message_index.append(alphabet.index(char))
            print(f"Символ сообщения: '{char}'\n"
                  f"Индекс символа в алфавите (m): {alphabet.index(char)}\n")

    return message_index


def find_Blind_Message(blind_factor, N, message_index):
    blind_message = []

    for i in message_index:
        blind_element = (blind_factor * i) % N
        blind_message.append(blind_element)

    return blind_message


def sign_Generation(blind_message, d, N):
    Sg = []

    for i in blind_message:
        rec = i
        sg_element = pow(rec, d, N)
        Sg.append(sg_element)

    return Sg


def verification():
    unblinded_signature = []
    for i in Sg:
        unblinded_element = (i * num2) % N
        unblinded_signature.append(unblinded_element)
    print(f"Убираем ослепление, получаем: {unblinded_signature}")

    verified, decrypted_message = decrypt_And_Compare(N, blind_factor, blind_message)

    if verified:
        print("Подпись действительна. Расшифрованное сообщение:", decrypted_message)
    else:
        print("Подпись недействительна!")


def decrypt_And_Compare(N, blind_factor, blind_message):
    original_message_index = []
    for i in blind_message:
        original_message_element = (i * inverse(blind_factor, N)) % N
        original_message_index.append(original_message_element)
    print(f"Расшифрованные индексы сообщения: {original_message_index} \n")

    decrypted_message = ""
    for l in original_message_index:
        decrypted_message += alphabet[l]
        print(f"Индекс символа в алфавите (m): {l}\n"
              f"Символ сообщения: '{alphabet[l]}'\n")

    if decrypted_message == message:
        return True, decrypted_message
    else:
        return False, decrypted_message


if __name__ == "__main__":
    print("Программа реализует алгоритм цифровой подписи RSA "
          "с дополнительными функциями по схеме слепой подписи.")
    print("Используемый алфавит:", alphabet, "\n")

    print("Нужно будет ввести разных два простых числа (p и q) больше 10")
    q = int(input("Введите простое число q: "))
    p = int(input("Введите простое число p: "))
    N = p * q

    public, private = generate_Keys()
    print("Публичный ключ (e, N):", public)
    print("Приватный ключ (d, N):", private)

    message = str(input("Введите сообщение: "))
    print()
    message_index = find_Index(message)
    print("Индексы символов из сообщения в алфавите: ", message_index)

    num1, num2 = rand_Pair(N)
    print("Рандомная пара чисел: num1 =", num1, " | num2 =", num2)

    blind_factor = inverse(num1, N)
    print("Ослепляющий(маскирующий) фактор: blind_factor =", blind_factor)

    blind_message = find_Blind_Message(blind_factor, N, message_index)
    print("Ослепленное(замаскированное) сообщение:", blind_message)

    Sg = sign_Generation(blind_message, private[0], N)
    print("Сгенерированная подпись:", Sg, "\n")

    choice = int(input("Если хотите проверить подпись, то введите число 1: "))

    if choice == 1:
        verification()
    else:
        print("Конец работы программы.")
