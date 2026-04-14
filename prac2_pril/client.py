import socket
import json

HOST = '217.71.129.139'
PORT = 4544

def send(cmd, data=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        request = {"command": cmd}
        if data:
            request["data"] = data
        if cmd == 'check' and data:
            request["zone"] = data
            
        sock.send(json.dumps(request).encode())
        response = sock.recv(2048).decode()
        sock.close()
        return json.loads(response)
    except socket.timeout:
        return {"status": "error", "message": "Сервер не отвечает"}
    except ConnectionRefusedError:
        return {"status": "error", "message": "Сервер недоступен"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    while True:
        print("\n" + "="*40)
        print("ПРОМЫШЛЕННАЯ БЕЗОПАСНОСТЬ")
        print("="*40)
        print("1. Правила безопасности")
        print("2. Последние инциденты")
        print("3. Проверка безопасности зоны")
        print("4. Сообщить об инциденте")
        print("0. Выход")
        
        choice = input("Выбор: ")
        
        if choice == '1':
            resp = send('rules')
            if resp['status'] == 'ok':
                print("\nПРАВИЛА БЕЗОПАСНОСТИ:")
                for r in resp['rules']:
                    print(f"  - {r}")
            else:
                print(f"Ошибка: {resp['message']}")
        
        elif choice == '2':
            resp = send('incidents')
            if resp['status'] == 'ok':
                print("\nПОСЛЕДНИЕ ИНЦИДЕНТЫ:")
                for i in resp['incidents']:
                    print(f"  {i['date']} | {i['location']}")
                    print(f"  {i['desc']}")
            else:
                print(f"Ошибка: {resp['message']}")
        
        elif choice == '3':
            zone = input("Введите название зоны/цеха: ")
            resp = send('check', zone)
            if resp['status'] == 'ok':
                print(f"\n{resp['message']}")
                print(f"Необходимые СИЗ: {', '.join(resp['required'])}")
            else:
                print(f"Ошибка: {resp['message']}")
        
        elif choice == '4':
            print("\nНОВЫЙ ИНЦИДЕНТ")
            date = input("Дата (ГГГГ-ММ-ДД): ")
            location = input("Место: ")
            desc = input("Описание: ")
            resp = send('report', {"date": date, "location": location, "desc": desc})
            if resp['status'] == 'ok':
                print(resp['message'])
            else:
                print(f"Ошибка: {resp['message']}")
        
        elif choice == '0':
            print("Завершение работы")
            break

if __name__ == '__main__':
    main()