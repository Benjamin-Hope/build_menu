#include <Calculator/example_calculator.h>

uint8_t Calculator::add(uint8_t x)
{
  m_value += x;
  return m_value;
}
