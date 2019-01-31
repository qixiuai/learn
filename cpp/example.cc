
#include <iostream>
#include <vector>
#include <string>


int main() {
  using namespace std;

  vector<unsigned char> data = {'1', '2', '3'};
  
  std::string str(data.begin(), data.begin()+2);
  std::cout << str << std::endl;

  std::string s{1,2,3, 'a'};
  std::cout << s << std::endl;

  vector<unsigned> dt(data.begin(), data.begin()+2);
  std::cerr << dt.size() << '\n';
  
  return 0;
}
