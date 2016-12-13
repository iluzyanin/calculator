# pylint: disable=C0103
# pylint: disable=C0111

import unittest
import calculator
from mock import MagicMock


class ParseTestCase(unittest.TestCase):

    def setUp(self):
        self.calculator = calculator.Calculator()

    def when_input_empty_string_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(ValueError, 'No input provided'):
            # act
            self.calculator.parse('')

    def when_parsing_expression_should_skip_spaces(self):
        # act
        result = self.calculator.parse('3 + 4 + 5')

        # assert
        self.assertEqual(result, [3, 4, '+', 5, '+'])

    def when_parsing_single_operation_should_put_numbers_first(self):
        # act
        result = self.calculator.parse('3+4')

        # assert
        self.assertEqual(result, [3, 4, '+'])

    def when_lower_precedence_operator_before_higher_should_put_lower_last(self):
        # act
        result = self.calculator.parse('3+4*5')

        # assert
        self.assertEqual(result, [3, 4, 5, '*', '+'])

    def when_higher_precedence_operator_before_lower_should_put_higher_between(self):
        # act
        result = self.calculator.parse('3*4+5')

        # assert
        self.assertEqual(result, [3, 4, '*', 5, '+'])

    def when_expression_with_parentheses_should_obey_precedence(self):
        # act
        result = self.calculator.parse('(3+4)*5')

        # assert
        self.assertEqual(result, [3, 4, '+', 5, '*'])

    def when_multidigit_expresssions_should_return_valid_rpn(self):
        # act
        result = self.calculator.parse('12 + 45 * 415')

        # assert
        self.assertEqual(result, [12, 45, 415, '*', '+'])

    def when_no_matching_opening_parentesis_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(SyntaxError, 'Could not find pair for "\)"'):
            # act
            self.calculator.parse('11 + 13) * 2')

    def when_no_matching_closing_parentesis_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(SyntaxError, 'Could not find pair for "\("'):
            # act
            self.calculator.parse('(11 + 13 * 2')

    def when_unknown_token_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(SyntaxError, 'Unknown token'):
            # act
            self.calculator.parse('11 + 13 # 2')


class ProcessRpnTestCase(unittest.TestCase):

    def setUp(self):
        self.calculator = calculator.Calculator()

    def when_input_empty_list_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(ValueError, 'Nothing to process'):
            # act
            self.calculator.process_rpn([])

    def when_processing_single_operation_should_return_valid_result(self):
        # act
        result = self.calculator.process_rpn([3, 4, '+'])

        # assert
        self.assertEqual(result, 7)

    def when_lower_precedence_operator_before_higher_should_process_higher_first(self):
        # act
        result = self.calculator.process_rpn([3, 4, 5, '*', '+'])

        # assert
        self.assertEqual(result, 23)

    def when_higher_precedence_operator_before_lower_should_process_higher_first(self):
        # act
        result = self.calculator.process_rpn([3, 4, '*', 5, '+'])

        # assert
        self.assertEqual(result, 17)

    def when_too_many_arguments_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(SyntaxError, 'Insufficient amount of operators'):
            # act
            self.calculator.process_rpn([3, 4, 5, '*'])

    def when_too_many_operators_should_raise_error(self):
        # assert
        with self.assertRaisesRegexp(SyntaxError, 'Insufficient amount of arguments'):
            # act
            self.calculator.process_rpn([3, 5, '*', '+'])


class EvaluateRpnTestCase(unittest.TestCase):

    def setUp(self):
        self.calculator = calculator.Calculator()

    def when_evaluating_expression_return_call_parse_and_process(self):
        # arrange
        self.calculator.parse = MagicMock(return_value=[2, 2, '+'])
        self.calculator.process_rpn = MagicMock(return_value=4)

        # act
        result = self.calculator.evaluate('2 + 2')

        # assert
        self.calculator.parse.assert_called_with('2 + 2')
        self.calculator.process_rpn.assert_called_with([2, 2, '+'])

    def when_evaluating_complex_expression_should_return_correct_result(self):
        # act
        result = self.calculator.evaluate('(15 + 7) / 2 - (65 - 61) * 2')

        # assert
        self.assertEqual(result, 3)

test_loader = unittest.TestLoader()
test_loader.testMethodPrefix = 'when'

parse_test_suite = test_loader.loadTestsFromTestCase(ParseTestCase)
process_test_suite = test_loader.loadTestsFromTestCase(ProcessRpnTestCase)
evaluate_test_suite = test_loader.loadTestsFromTestCase(EvaluateRpnTestCase)

test_suite = unittest.TestSuite(
    [parse_test_suite, process_test_suite, evaluate_test_suite])
unittest.TextTestRunner(verbosity=2).run(test_suite)
