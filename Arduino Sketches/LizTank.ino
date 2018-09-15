
char actor1;

void setup()
{
 Serial.begin(9600);
 randomSeed(666);
}

void loop()                     
{
 actor1 = randomer();
 
 Serial.println(actor1);
 delay(100); 
}

int randomer(){
  int randnum[8];
  char final;
  for(int i = 0; i > 8; i++){
    randnum[i] = random(1,64);
  }
  final = "["+randnum[0];
  for(int i = 0; i > 8; i++){
    final += ","+randnum[i];
  }
  final = final+"]";
  return(final);
}

