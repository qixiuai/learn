#include <stdio.h>
#include "kitty.h"

kitty::kitty(){
  printf("Constructor\n");
  variable = 100;
}

kitty::~kitty(){
  printf("Destructor\n");
  variable = 0;
}

void kitty::speak(){
  printf("I'm a cat.\n");
}
