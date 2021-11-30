from src.calculator_utils import (
    calculate,
    check_invalid_operator,
    check_invalid_operands,
)
import nose
from nose.tools import raises, assert_true, assert_false


class TestCalculate:
    ## operator == "+"
    def test_positive_number_add_positive_number(self):
        assert calculate("+", [1, 3]) == 4

    def test_positive_number_add_negative_number(self):
        assert calculate("+", [1, -3]) == -2

    def test_negative_number_add_negative_number(self):
        assert calculate("+", [-1, -1]) == -2

    def test_zero_add_positive_number(self):
        assert calculate("+", [0, 3]) == 3

    def test_zero_add_negative_number(self):
        assert calculate("+", [0, -1]) == -1

    ## operator == "-"
    def test_positive_number_subtract_positive_number(self):
        assert calculate("-", [1, 3]) == -2

    def test_positive_number_subtract_negative_number(self):
        assert calculate("-", [1, -3]) == 4

    def test_negative_number_subtract_negative_number(self):
        assert calculate("-", [-1, -1]) == 0

    def test_zero_subtract_positive_number(self):
        assert calculate("-", [0, 3]) == -3

    def test_zero_subtract_negative_number(self):
        assert calculate("-", [0, -1]) == 1

    ## operator == "*"
    def test_positive_number_multiply_positive_number(self):
        assert calculate("*", [2, 3]) == 6

    def test_positive_number_multiply_negative_number(self):
        assert calculate("*", [2, -3]) == -6

    def test_negative_number_multiply_negative_number(self):
        assert calculate("*", [-3, -4]) == 12

    def test_one_multiply_positive_number(self):
        assert calculate("*", [1, 4]) == 4

    def test_one_multiply_negative_number(self):
        assert calculate("*", [1, -2]) == -2

    def test_zero_multiply_positive_number(self):
        assert calculate("*", [0, 4]) == 0

    def test_zero_multiply_negative_number(self):
        assert calculate("*", [0, -3]) == 0

    ## operator == "/"
    def test_positive_number_divide_positive_number_no_remainder(self):
        assert calculate("/", [4, 2]) == 2

    def test_positive_number_divide_positive_number_with_remainder(self):
        assert calculate("/", [3, 2]) == 1.5

    def test_positive_number_divide_negative_number_no_remainder(self):
        assert calculate("/", [2, -1]) == -2

    def test_positive_number_divide_negative_number_with_remainder(self):
        assert calculate("/", [5, -2]) == -2.5

    def test_negative_number_divide_negative_number_no_remainder(self):
        assert calculate("/", [-4, -2]) == 2

    def test_negative_number_divide_negative_number_with_remainder(self):
        assert calculate("/", [-3, -2]) == 1.5

    def test_zero_divide_positive_number(self):
        assert calculate("/", [0, 2]) == 0

    def test_zero_divide_negative_number(self):
        assert calculate("/", [0, -3]) == 0

    @raises(ValueError)
    def test_positive_number_divide_zero(self):
        calculate("/", [2, 0])

    @raises(ValueError)
    def test_negative_number_divide_zero(self):
        calculate("/", [-3, 0])

    @raises(ValueError)
    def test_zero_divide_zero(self):
        calculate("/", [0, 0])

class TestCheckInvalidOperator:
    def test_add_operator(self):
        assert_false(check_invalid_operator("+"))

    def test_subtract_operator(self):
        assert_false(check_invalid_operator("-"))

    def test_multiply_operator(self):
        assert_false(check_invalid_operator("*"))

    def test_divide_operator(self):
        assert_false(check_invalid_operator("/"))

    def test_empty_string_operator(self):
        assert_true(check_invalid_operator(""))

    def test_exclamation_operator(self):
        assert_true(check_invalid_operator("!"))

    def test_double_add_operator(self):
        assert_true(check_invalid_operator("++"))

    def test_integer_operator(self):
        assert_true(check_invalid_operator(0))


class TestCheckInvalidOperands:
    def test_two_integer_operands(self):
        assert_false(check_invalid_operands([1, 3]))

    def test_two_float_operands(self):
        assert_false(check_invalid_operands([1.0, 3.0]))

    def test_one_integer_operand_one_float_operand(self):
        assert_false(check_invalid_operands([2, 3.0]))

    def test_two_string_operands(self):
        assert_true(check_invalid_operands(["1", "3"]))

    def test_one_string_operand_one_integer_operand(self):
        assert_true(check_invalid_operands(["1", 3]))

    def test_one_string_operand_one_float_operand(self):
        assert_true(check_invalid_operands(["1", 3.0]))

    def test_three_integer_operands(self):
        assert_true(check_invalid_operands([1, 2, 3]))

    def test_two_integer_one_string_operands(self):
        assert_true(check_invalid_operands([1, 3, "a"]))

    def test_empty_list_operands(self):
        assert_true(check_invalid_operands([]))
