
#include <iostream>

int add(int a, int b) {
  return a;
}

int add(float a, float b) {
  return a + 10;
}

int add(double a, double b) {
  return a+100;
}

int add(int a) {
  return 0;
}
  
int main() {
  float a = 1;
  float b = 1;
  auto ret = add(a);
  std::cout << ret << '\n';
  return 0;
}
