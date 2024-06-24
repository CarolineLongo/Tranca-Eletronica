import cv2
import face_recognition
import serial
import time
import os

# Configuração da conexão serial com o Arduino
arduino = serial.Serial('COM4', 9600)  # Substitua 'COM4' pela porta correta
time.sleep(2)  # Tempo para estabilizar a conexão serial

# Carregamento do classificador de Haar para reconhecimento facial
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Carregar fotos de pessoas cadastradas
known_face_encodings = []
known_face_names = []

def carregar_faces_conhecidas(diretorio_faces_conhecidas):
    for nome_arquivo in os.listdir(diretorio_faces_conhecidas):
        if nome_arquivo.endswith(".jpg") or nome_arquivo.endswith(".png"):
            caminho_imagem = os.path.join(diretorio_faces_conhecidas, nome_arquivo)
            imagem = face_recognition.load_image_file(caminho_imagem)
            codificacao = face_recognition.face_encodings(imagem)
            if codificacao:
                known_face_encodings.append(codificacao[0])
                known_face_names.append(os.path.splitext(nome_arquivo)[0])

# Diretório onde as fotos cadastradas estão armazenadas
diretorio_faces_conhecidas = "C:/Users/carol/OneDrive/Área de Trabalho/Trabalho IOT/faces_conhecidas"  # Exemplo de caminho no Windows

carregar_faces_conhecidas(diretorio_faces_conhecidas)

# Inicialização da variável da câmera
cap = None

while True:
    if arduino.in_waiting > 0:
        linha = arduino.readline().decode('utf-8').strip()
        if linha == "MOTION DETECTED":
            if cap is None:
                cap = cv2.VideoCapture(0)  # Ativa a câmera
                print("Câmera ativada")
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                rosto_reconhecido = False
                for codificacao_rosto in face_encodings:
                    coincidencias = face_recognition.compare_faces(known_face_encodings, codificacao_rosto)
                    if True in coincidencias:
                        indice_primeira_coincidencia = coincidencias.index(True)
                        nome = known_face_names[indice_primeira_coincidencia]
                        rosto_reconhecido = True
                        break

                if rosto_reconhecido:
                    for (topo, direita, baixo, esquerda) in face_locations:
                        cv2.rectangle(frame, (esquerda, topo), (direita, baixo), (0, 255, 0), 2)
                    if arduino.is_open:
                        arduino.write(b'ACTIVATE SERVO\n')
                else:
                    if arduino.is_open:
                        arduino.write(b'NO FACE DETECTED\n')
                    for (topo, direita, baixo, esquerda) in face_locations:
                        cv2.rectangle(frame, (esquerda, topo), (direita, baixo), (0, 0, 255), 2)

                cv2.imshow('Câmera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if arduino.in_waiting > 0:
                    linha = arduino.readline().decode('utf-8').strip()
                    if linha == "MOTION ENDED":
                        break
            cap.release()
            cv2.destroyAllWindows()
            cap = None
            print("Câmera desativada")
            
# Libera a câmera e fecha a janela se estiver ativa
if cap is not None:
    cap.release()
cv2.destroyAllWindows()
if arduino.is_open:
    arduino.close()
