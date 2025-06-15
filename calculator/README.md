# Calculator README

This document explains how the calculator evaluates expressions, applies operators, and manages the display.

## Expression Evaluation (Infix Notation)

The calculator evaluates expressions written in infix notation (e.g., `2 + 3 * 4`). Here's a breakdown:

1.  **Tokenization:** The input string is first broken down into a sequence of tokens. Each token represents a number, operator, or parenthesis.
2.  **Shunting Yard Algorithm:** The calculator uses a variation of the Shunting Yard algorithm to convert the infix notation into postfix notation (also known as Reverse Polish Notation or RPN).
    *   Numbers are directly added to the output queue.
    *   Operators are pushed onto an operator stack. The order operators are pushed onto the stack depends on precedence. Higher precedence operators are pushed onto the stack before lower precedence operators.
    *   Left parentheses are pushed onto the stack.
    *   Right parentheses cause operators to be popped from the stack and added to the output queue until a left parenthesis is encountered. The left parenthesis is then discarded.
3.  **Postfix Evaluation:** The postfix expression (RPN) is evaluated using a stack.
    *   Numbers are pushed onto the stack.
    *   When an operator is encountered:
        *   The required number of operands are popped from the stack (e.g., two for binary operators like `+`, `-`, `*`, `/`).
        *   The operator is applied to the operands.
        *   The result is pushed back onto the stack.
4.  **Final Result:** After processing the entire postfix expression, the final result remains on the stack.

## Operator Application

The calculator supports standard arithmetic operators: `+` (addition), `-` (subtraction), `*` (multiplication), and `/` (division).

Operator precedence is handled as follows:

1.  Multiplication and division have higher precedence than addition and subtraction.
2.  Parentheses can be used to override the default precedence.

When an operator is applied, the appropriate arithmetic operation is performed on the operands. Division by zero is prevented and results in an error.

## Display

The calculator display shows the current expression being entered and the result of the evaluation. The display is updated as follows:

1.  **Input:** As numbers and operators are entered, they are appended to the expression displayed on the screen.
2.  **Evaluation:** When the user triggers the evaluation (e.g., by pressing an equals button), the expression is evaluated as described above, and the result is displayed.
3.  **Error Handling:** If an error occurs during evaluation (e.g., division by zero, invalid expression), an error message is displayed.
4.  **Clearing:** The display can be cleared to start a new calculation.