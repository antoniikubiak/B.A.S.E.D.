#include <stdio.h>

double compile_exp(double val);
double compute_gradient(double w, double x, double y);
double optimize_cbrt(double initial_guess, double radicand, int max_steps);

int main() {
    printf("B.A.S.E.D. Execution Demo\n\n");

    double x_val = 1.0;
    double exp_result = compile_exp(x_val);
    printf("[Example 1] Taylor Series e^(%0.1f) approximation: %0.5f (Expected ~2.71828)\n", x_val, exp_result);

    double weight = 0.5;
    double input = 2.0;
    double target_y = 1.0;
    double gradient = compute_gradient(weight, input, target_y);
    printf("[Example 2] Backprop Loss Gradient wrt:     %0.5f\n", gradient);

    double guess = 2.0;
    double radicand = 10.0;
    int steps = 8;
    double cbrt_result = optimize_cbrt(guess, radicand, steps);
    printf("[Example 3] Newton-Raphson Cube Root of %0.1f:      %0.5f (Expected ~2,15443469)\n\n", radicand, cbrt_result);

    return 0;
}
