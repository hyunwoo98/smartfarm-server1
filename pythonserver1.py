import socket
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

HOST = "192.168.0.76"
PORT = 3889
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
s.bind((HOST, PORT))
print ('Socket bind complete')
s.listen(1)
print ('Socket now listening')

#파이 컨트롤 함수
def do_some_stuffs_with_input(input_string):
   #라즈베리파이를 컨트롤할 명령어 설정
   if input_string == "led":
      input_string = "led를 점등합니다."
      GPIO.output(23, True)
      time.sleep(1)
      GPIO.output(23, False)
      time.sleep(1)
   elif input_string == "pump":
      input_string = "펌프를 작동시킵니다."
   elif input_string == "fan":
      input_string = "팬을 작동시킵니다."
   else :
      input_string = input_string + " 없는 명령어 입니다."
   return input_string

while True:
   #접속 승인
   conn, addr = s.accept()
   print("Connected by ", addr)

   #데이터 수신
   data = conn.recv(1024)
   data = data.decode("utf8").strip()
   if not data: break
   print("Received: " + data)

   #수신한 데이터로 파이를 컨트롤 
   res = do_some_stuffs_with_input(data)
   print("파이 동작 :" + res)

   #클라이언트에게 답을 보냄
   conn.sendall(res.encode("utf-8"))
   #연결 닫기
   conn.close()
s.close()