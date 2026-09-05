#include <gtest/gtest.h>
#include <Calculator/example_calculator.h>

TEST(Calculator, AddsTwoNumbers)
{
  Calculator calc;
  EXPECT_NO_THROW(calc.add(2));
}