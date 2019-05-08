/*
Measuring Current Using ACS712
*/
const int analogIn = A0;
int mVperAmp = 185; // use 100 for 20A Module and 66 for 30A Module
int RawValue= 0;
int ACSoffset = 2500; 
double Voltage = 0;
double Amps = 0;
int Amps_inter = 0;
char Amps_new[50] = {0};
int filter[11] = {0};
int sum = 0;
float mean_filter;
int i;

void setup(){ 
 Serial.begin(9600);
}

void loop(){
  
  //int t1 = millis();
 
 RawValue = analogRead(analogIn);
 //Voltage = (RawValue / 1024.0) * 5000; // Gets you mV
 //Amps = ((Voltage - ACSoffset) / mVperAmp);
 sum = 0;
 for(i = 0; i<= 9; i++)
 {
  filter[i] = filter[i+1];
  sum = sum + filter[i];
  //Serial.println(filter[i]);
 }
 filter[i] = RawValue;
 mean_filter  = (sum + filter[i])/11;
 
 Voltage = (mean_filter / 1024.0) * 5000; // Gets you mV
 Amps = ((Voltage - ACSoffset) / mVperAmp)/0.7;
 Amps_inter =  Amps*10; //needed integer type for conversion to char type so had to do this
 sprintf(Amps_new,"%02X",Amps_inter);
 
 //Serial.print("Raw Value = " ); // shows pre-scaled value 
 //Serial.print(mean_filter); 
 //Serial.print("\t mV = "); // shows the voltage measured 
 //Serial.print(Voltage,3); // the '3' after voltage allows you to display 3 digits after decimal point
 //Serial.print("\t Amps = "); // shows the voltage measured 
 Serial.println(Amps_new); // the '3' after voltage allows you to display 3 digits after decimal point
 //delay(10);  
 //int t2 = millis();
 //int t = t2 - t1;
 //Serial.print("Time taken in milliseconds = ");
 //Serial.println(t,6);
 //delay(1000);
}
