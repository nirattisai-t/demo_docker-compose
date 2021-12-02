def calculate(operator: str, operands: list):
    if operator == "+":
        result = operands[0] + operands[1]

    elif operator == "-":
        result = operands[0] - operands[1]

    elif operator == "*":
        result = operands[0] * operands[1]

    elif operator == "/":
        if operands[1] == 0:
            raise ValueError("Zero Division Occurs")

        result = operands[0] / operands[1]

    return result


def check_invalid_operator(operator: str):
    if operator not in ["+", "-", "*", "/"]:
        return True
    else:
        return False


def check_invalid_operands(operands: list):
    # check that operands are int or float and len == 2
    list_check = [isinstance(operand, (int, float)) for operand in operands]

    if len(operands) == 2 and sum(list_check) == 2:
        return False
    else:
        return True
