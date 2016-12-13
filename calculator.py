# pylint: disable=C0111


# TODO: When it will come to associativity, this may come in handy
class Operator():

    def __init__(self, symbol, precedence, associativity):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity


class Calculator():

    def __init__(self):
        self.operatorsByPrecedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def parse(self, inputstr):
        if not inputstr:
            raise ValueError('No input provided')

        index = 0
        operators = []
        output = []
        while index < len(inputstr):
            current_token = inputstr[index]
            if current_token.isdigit():
                current_number = current_token
                while (index < len(inputstr) - 1) and inputstr[index + 1].isdigit():
                    index += 1
                    current_number += inputstr[index]
                output.append(int(current_number))
            elif self.operatorsByPrecedence.has_key(current_token):
                operator_index = len(operators) - 1
                while operator_index >= 0 and \
                        operators[operator_index] <> '(' and \
                        self.operatorsByPrecedence[current_token] <= \
                        self.operatorsByPrecedence[operators[operator_index]]:
                    output.append(operators.pop())
                    operator_index -= 1
                operators.append(current_token)
            elif current_token == '(':
                operators.append(current_token)
            elif current_token == ')':
                operator_index = len(operators) - 1
                while operator_index >= 0 and \
                        operators[operator_index] <> '(':
                    output.append(operators.pop())
                    operator_index -= 1
                if operator_index < 0:
                    raise SyntaxError(
                        'Could not find pair for ")" at index {0}'.format(index))
                operators.pop()
            elif current_token == ' ':
                pass
            else:
                raise SyntaxError(
                    'Unknown token "{0}" at index {1}'.format(current_token, index))
            index += 1
        while operators:
            operator = operators.pop()
            if operator == '(':
                raise SyntaxError('Could not find pair for "("')
            output.append(operator)

        return output

    def process_rpn(self, parsed_tokens):
        if len(parsed_tokens) == 0:
            raise ValueError('Nothing to process')
        index = 0
        values = []
        while index < len(parsed_tokens):
            current_token = parsed_tokens[index]
            if type(current_token).__name__ == 'int':
                values.append(current_token)
            elif self.operatorsByPrecedence.has_key(current_token):
                if len(values) < 2:
                    raise SyntaxError('Insufficient amount of arguments')
                right = values.pop()
                left = values.pop()
                if current_token == '+':
                    values.append(left + right)
                elif current_token == '-':
                    values.append(left - right)
                elif current_token == '*':
                    values.append(left * right)
                elif current_token == '/':
                    values.append(left / right)
            index += 1

        if len(values) == 1:
            return values[0]

        raise SyntaxError('Insufficient amount of operators')

    def evaluate(self, inputstr):
        return self.process_rpn(self.parse(inputstr))
