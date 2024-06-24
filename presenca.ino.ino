#include <Servo.h>

int pirPin = 2; // Pino de entrada do sensor PIR
int ledGreenPin = 13; // Pino de saída do LED verde
int ledRedPin = 12; // Pino de saída do LED vermelho
int servoPin = 9; // Pino de saída do servo motor

Servo meuServo;
bool movimentoDetectado = false;

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(ledGreenPin, OUTPUT);
  pinMode(ledRedPin, OUTPUT);
  Serial.begin(9600); // Inicializa a comunicação serial a 9600 bps
  meuServo.attach(servoPin);
  meuServo.write(0); // Posiciona o servo na posição inicial
}

void loop() {
  int estadoPir = digitalRead(pirPin);
  if (estadoPir == HIGH && !movimentoDetectado) {
    Serial.println("MOVIMENTO DETECTADO"); // Envia mensagem serial
    movimentoDetectado = true;
  } else if (estadoPir == LOW && movimentoDetectado) {
    Serial.println("MOVIMENTO TERMINADO"); // Envia mensagem serial
    movimentoDetectado = false;
  }
  
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    if (comando == "ATIVAR SERVO") {
      digitalWrite(ledGreenPin, HIGH); // Acende o LED verde
      meuServo.write(90); // Gira o servo para a posição de 90 graus
      delay(1000); // Espera 1 segundo
      meuServo.write(0); // Retorna o servo para a posição inicial
      digitalWrite(ledGreenPin, LOW); // Apaga o LED verde
    } else if (comando == "NENHUM ROSTO DETECTADO") {
      digitalWrite(ledRedPin, HIGH); // Acende o LED vermelho
      delay(1000); // Mantém o LED vermelho aceso por 1 segundo
      digitalWrite(ledRedPin, LOW); // Apaga o LED vermelho
    }
  }

  delay(100); // Atraso para evitar leitura instável
}
