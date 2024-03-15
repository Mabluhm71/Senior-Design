
#define encoderPin 2
#define PIN_OUTPUT 6
// Define variables
unsigned int pulseCount = 0;
unsigned int pulseCountOld = 0; // Variable to store the number of pulses
unsigned long prevTime = 0;  // Variable to store the previous time
float rpm = 0;  // Variable to store the calculated RPM
double last_time;
double integral, previous, output = 0;
double kp, ki, kd;
double factor = 1;
double setpoint = 75.00;
float error =0;
float dt;
const float PPR_inv= 1/2048; 
float errorOld=0;

void setup() {
  kp = 0.8;
  ki = 0.20;
  kd = 0.001;
  last_time = 0;
  Serial.begin(9600);
  analogWrite(PIN_OUTPUT, 0);
  // Set up the encoder pin as an input
  pinMode(encoderPin, INPUT);
  
  // Attach an interrupt to the encoder pin that triggers on a rising edge
  attachInterrupt(digitalPinToInterrupt(encoderPin), pulseCounter, RISING);

  // Initialize the serial communication
  Serial.begin(9600);
}

void loop() {

  // Initialize the Serial interface:

if (Serial.available() > 0) {
int inByte = Serial.read();

  switch (inByte) {

  
  case '1': 
    factor = factor*-1;
  break;
  
  case '2': 
    factor = .1;
  break;

  case '3': 
    factor = 1;
  break;

  case '4': // 
    factor = 10;
  break;

  case '5': 
    kp = kp+factor;
  break;

  case '6': 
    ki = ki+factor;
  break;

  case '7': 
    kd = kd+factor;
  break;
  
  }
}
  double now = millis();
  dt = (now - last_time)*0.001;
  last_time = now;

  // Calculate RPM and print it
  unsigned long currentTime = millis();
    int Diff = pulseCount-pulseCountOld;
    pulseCountOld = pulseCount;
    rpm = (Diff*PPR_inv)/dt;
    
    pulseCount = 0;  // Reset pulse count
    prevTime = currentTime;

    
  //PID
  error = rpm - setpoint;
  
  float P=kp*error;
  float D=kd*(error-errorOld/dt);
  float I=ki*dt*.05*(error-errorOld);
  errorOld=error;
  float output =P+I+D;
  if (output > 0){
    if (output > 255){
      analogWrite(PIN_OUTPUT, 255);
    }else 
    analogWrite(PIN_OUTPUT, output);
  }else
  analogWrite(PIN_OUTPUT, output);
  //PID  
  

  // Setpoint VS Actual
  Serial.print(setpoint);
  Serial.print(",");
  Serial.println(rpm);
}
void pulseCounter() {
  pulseCount++;
}
