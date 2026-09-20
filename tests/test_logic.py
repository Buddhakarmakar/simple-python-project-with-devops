import pytest

from calculator.logic import (
    to_python_expression,
    to_display_expression,
    format_result,
    safe_eval,
    evaluate_display_expression,
)


class TestSymbolConversion:
    def test_to_python_expression_converts_all_symbols(self):
        assert to_python_expression("2×3÷4−1") == "2*3/4-1"

    def test_to_python_expression_leaves_plain_numbers_untouched(self):
        assert to_python_expression("123+45") == "123+45"

    def test_to_display_expression_converts_operators(self):
        assert to_display_expression("2*3/4-1") == "2×3÷4−1"


class TestFormatResult:
    def test_whole_number_float_drops_decimal(self):
        assert format_result(4.0) == "4"

    def test_non_whole_float_is_rounded(self):
        assert format_result(1 / 3) == "0.3333333333"

    def test_integer_passthrough(self):
        assert format_result(42) == "42"


class TestSafeEval:
    def test_basic_addition(self):
        assert safe_eval("2+2") == 4

    def test_operator_precedence(self):
        assert safe_eval("2+3*4") == 14

    def test_division(self):
        assert safe_eval("10/4") == 2.5

    def test_division_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            safe_eval("5/0")

    def test_empty_expression_raises_value_error(self):
        with pytest.raises(ValueError):
            safe_eval("")

    def test_disallowed_characters_raise_value_error(self):
        with pytest.raises(ValueError):
            safe_eval("__import__('os')")

    def test_disallowed_letters_raise_value_error(self):
        with pytest.raises(ValueError):
            safe_eval("2+abc")


class TestEvaluateDisplayExpression:
    def test_simple_expression(self):
        assert evaluate_display_expression("2+2") == "4"

    def test_expression_with_display_symbols(self):
        assert evaluate_display_expression("6×7") == "42"

    def test_division_by_zero_returns_friendly_error(self):
        assert evaluate_display_expression("5÷0") == "Error: ÷0"

    def test_invalid_expression_returns_error(self):
        assert evaluate_display_expression("2++") == "Error"
