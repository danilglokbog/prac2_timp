import socket
import json

HOST = '172.17.10.235'
PORT = 5333

SAFETY_RULES = [
    "Использование СИЗ (каска, очки, перчатки) обязательно",
    "Работа на высоте только со страховкой",
    "Электроустановки только с допуском",
    "Курение в специально отведенных местах"
]

INCIDENTS = [
    {"date": "2025-03-15", "location": "Цех N3", "desc": "Падение груза с крана"},
    {"date": "2025-03-10", "location": "Склад ГСМ", "desc": "Разлив масла, устранено"}
]

def handle_request(data):
    try:
        request = json.loads(data)
        cmd = request.get('command')
        
        if cmd == 'rules':
            return json.dumps({"status": "ok", "rules": SAFETY_RULES})
        
        elif cmd == 'incidents':
            return json.dumps({"status": "ok", "incidents": INCIDENTS})
        
        elif cmd == 'check':
            zone = request.get('zone', 'не указана')
            return json.dumps({
                "status": "ok",
                "message": f"Зона {zone} проверена",
                "required": ["Каска", "Жилет", "Ботинки"]
            })
        
        elif cmd == 'report':
            incident = request.get('data', {})
            INCIDENTS.append(incident)
            return json.dumps({"status": "ok", "message": "Инцидент зарегистрирован"})
        
        else:
            return json.dumps({"status": "error", "message": "Неизвестная команда"})
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(3)
    print(f"Сервер запущен на {HOST}:{PORT}")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Подключение от {addr}")
        
        data = conn.recv(2048).decode()
        print(f"Получены данные: {data}")
        
        if data:
            response = handle_request(data)
            print(f"Отправка ответа: {response[:100]}")
            conn.send(response.encode())
        else:
            print("Данные не получены")
        
        conn.close()
        print("Соединение закрыто\n")

if __name__ == '__main__':
    main()