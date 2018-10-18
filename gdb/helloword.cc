#include <iostream>
#include <vector>
#include <string>


int add(int a, int b) {
  return a + b;
}

int main() {
  int a = 1;
  int b = 2;
  int c = add(a, b);

  std::cout << c << std::endl;
  
  return 0;
}
