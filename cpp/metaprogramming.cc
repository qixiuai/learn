
#include <iostream>

template <int n>
struct factorial {
  enum data { ret = factorial<n-1>::ret * n };
};

template <>
struct factorial<0> { enum { ret = 1}; };

int main() {
  std::cout << factorial<20>::data::ret << std::endl;

  return 0;
}
