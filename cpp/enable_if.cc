#include <iostream>
#include <type_traits>

class foo;
class bar;

template<class T>
struct is_bar
{
    template<class Q = T>
    typename std::enable_if<std::is_same<Q, bar>::value, bool>::type check()
    {
        return true;
    }

    template<class Q = T>
    typename std::enable_if<!std::is_same<Q, bar>::value, bool>::type check()
    {
        return false;
    }

};

int main()
{
    is_bar<foo> foo_is_bar;
    is_bar<bar> bar_is_bar;
    if (!foo_is_bar.check() && bar_is_bar.check())
        std::cout << "It works!" << std::endl;

    return 0;
}
