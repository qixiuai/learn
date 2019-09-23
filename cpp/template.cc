
#include <type_traits>
#include <iostream>
#include <vector>

template <class C, class T=typename C::value_type>
T diff(C arr) {
  T a;
  return a;
}


int main() {

  std::vector<int> vec = {1,2,3,4,5,6};
  diff(vec);
  
  return 0;
}

