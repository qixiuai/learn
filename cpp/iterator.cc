
#include <iostream>
#include <string>
#include <vector>

int main() {

  struct A {
    int a;
  };
  
  std::vector<A> vec{A{1},A{2}};
  std::cout << vec.begin()->a << '\n';
  
  return 0;
}








