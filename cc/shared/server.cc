#include <string>
#include <iostream>
#include "server.h"

void print1(char* str, int size) {
  std::string addr(str, size);
  std::cerr << addr;
}
  

