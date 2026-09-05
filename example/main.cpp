#include <fmt/core.h>
#include <Calculator/example_calculator.h>

int main()
{
  fmt::print("Hello from Conan + C++!\n");

  Calculator instance;
  instance.add(2);
  return 0;
}
