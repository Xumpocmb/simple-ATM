def authorize():
    pin = input('Введите ПИН-код: ')
    clients = read_client_file()
    for client in clients:
        if pin == client.split(';')[1]:
            return client
        else:
            print('не правильный ПИН-код')
            main()


def read_client_file():
    with open('clients.csv', 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    return lines


def write_client_file(client_data):
    # считываем всех клиентов
    clients = read_client_file()
    # ищем клиента по ПИН
    for key, client in enumerate(clients):
        if not client:
            break
        else:
            if client.split(';')[1] == client_data.split(';')[1]:
                # обновляем данные клиента
                clients[key] = client_data
    # записываем новые данные в файл
    with open('clients.csv', 'w', encoding='utf-8') as file:
        file.write('\n'.join(clients))


def account_refill(client):
    client_data = client.split(';')
    balance = int(client_data[2])

    print(client.split(';')[0])
    print(f'Ваш баланс: {client.split(";")[2]}$')

    sum_for_refill = int(input('Введите сумму для пополнения: '))
    balance += sum_for_refill
    client_data[2] = str(balance)
    print(f'Остаток на балансе: {balance}')
    client = ';'.join(client_data)
    write_client_file(client)
    return client


def withdraw(client):
    client_data = client.split(';')
    balance = float(client_data[2])

    print(client_data[0])
    print(f'\nВаш баланс: {client_data[2]}$')

    sum_for_withdraw = float(input('Введите сумму для вывода: '))

    if sum_for_withdraw % 50 == 0:
        if sum_for_withdraw <= balance:
            print(f'\nВыдача {sum_for_withdraw}$')

            # процент за снятие
            percent = 0.015
            # изменение процента от суммы
            if sum_for_withdraw > 5000000:
                percent = 0.1

            # расчет суммы процента
            sum_percent = sum_for_withdraw * percent
            if sum_percent < 30:
                sum_percent = 30
            elif sum_percent > 600:
                sum_percent = 600

            # обновление баланса клиента после выдачи средств
            balance -= (sum_for_withdraw + sum_percent)
            print(f'Остаток на балансе: {balance}\nПроцент за снятие: {sum_percent}')

            # обновление информации о данных третьей операции
            third_operation = int(client_data[3])
            if third_operation == 3:
                print(f'Бонус за 3ю операцию: {balance * 0.03}')
                balance += balance * 0.03
                third_operation = 0
                client_data[3] = str(third_operation)
            else:
                third_operation += 1
                client_data[3] = str(third_operation)

            # подготовка информации к записи в файл
            client_data[2] = str(balance)
            client = ';'.join(client_data)
            write_client_file(client)
            return client
        else:
            print('\nНедостаточно средств!')
            return
    else:
        print('Сумма должна быть кратна 50!')
        return client


def main():
    client = authorize()
    while True:
        print(f'\nЗдравствуйте, {client.split(";")[0]}')
        print('\tМЕНЮ:')
        print('\t1 - снятие средств')
        print('\t2 - пополнение средств')
        print('\t4 - просмотр баланса')
        print('\t0 - выход')
        choice = input('Ваш выбор: ')

        match choice:
            case '1':
                client = withdraw(client)
            case '2':
                client = account_refill(client)
            case '4':
                print(client.split(";")[2])
            case '0':
                break
            case _:
                continue


if __name__ == '__main__':
    main()

