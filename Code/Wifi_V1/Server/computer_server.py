import socket             
   
s = socket.socket()       
print ("Socket successfully created") 
  
port = 12345

s.bind(('127.0.0.1', port))
print("Socket:", s.getsockname())

s.listen(1)
machineID = ""

while True:
    try:
        pico, addr = s.accept()
        machineID = pico.recv(2048).decode() #Pico ID
        print("Pico", machineID, "Connected")
        while True:
            data = pico.recv(2048).decode()
            print(data)
            if data == 'QUIT':
                break
    except:
        continue
    
    # Close the connection with the client
    pico.close() 