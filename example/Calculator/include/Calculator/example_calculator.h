// This serves only as an example for other service test and functionalities

#pragma once
#include <cstdint>

class Calculator
{
  public:
    Calculator() = default;
    ~Calculator() = default;

    uint8_t add(uint8_t x);

  private:
    uint8_t m_value {0};
};
