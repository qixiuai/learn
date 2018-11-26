using System;
using System.Collections.Generic;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
	    int a = 18;
	    int b = 6;
	    int c = a + b;
	    var list = new List<string> {"AA", "BB", "CC"};
	    foreach (var name in list)
	    {
		Console.WriteLine($"Hello World! {name}");
	    }
        }
    }
}
