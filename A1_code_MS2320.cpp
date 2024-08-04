#include <bits/stdc++.h>
using namespace std;
int f_x(int x)
{
    return (pow(x, 3) - (3 * pow(x, 2)) + 7);
}
double goldenRatio(int a, int b)
{
    int rho = 0.382;
    int t = 1 - rho;
    int tol = pow(10, -3);

    int c = a + (rho * (b - a));
    int d = a + (t * (b - a));

    int f_a = f_x(a);
    int f_b = f_x(b);
    int f_c = f_x(c);
    int f_d = f_x(d);

    while (true)
    {
        if (abs(a - b) > tol)
            return ((a + b) / 2);

        if (f_c < f_d)
        {
            b = d;
            f_b = f_d;
            d = c;
            f_d = f_c;
            c = a + (rho * (b - a));
            f_c = f_x(c);
        }
        else
        {
            a = c;
            f_a = f_c;
            c = d;
            f_c = f_d;
            d = a + (t * (b - a));
            f_d = f_x(d);
        }
    }
}
int main()
{
    double res = goldenRatio(1, 3);
    cout << "The value of minimizer :: " << res << endl;
    return 0;
}