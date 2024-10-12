import numpy as np


# TODO: Fix this so that symbolic variables can be used
class SymbolicVariable:
    def __init__(self, coeffs=None, vars=None, orders=None):
        if orders is None:
            orders = [1]
        if coeffs is None:
            coeffs = [1]
        if vars is None:
            vars = ["a"]
        self._vars = vars
        self._coeffs = coeffs
        self._orders = orders

    @property
    def var(self):
        return self._vars

    @property
    def coeff(self):
        return self._coeffs

    def __add__(self, other):
        new_term = SymbolicVariable()
        for term in self._vars:
            if term not in other._vars:
                return SymbolicVariable([self._coeffs, other._coeffs], [self._vars, other._vars], [self._orders, other._orders])
            else:
                return SymbolicVariable([self._coeffs + other._coeff], self._vars, self._orders)

    def __mul__(self, other):
        #if self._var != other._var:
            #result = MixedTerm((self._coeff*other._coeff), [self._var, other._var], [self._order, other._order])
        #else:
            #result = SymbolicVariable()
        return None


class Polynomial:
    def __init__(self, order: int = 1, coeffs=None):
        if coeffs is None:
            coeffs = np.zeros(order+1)
        if order < 0:
            raise ValueError("Order must be a positive integer")
        if len(coeffs) != (order + 1):
            raise ValueError("Order must match given coefficients")
        self._order = order
        self._coeffs = np.array(coeffs)

    @property
    def order(self):
        return self._order

    def __getitem__(self, index):
        if index > self._order:
            return IndexError("Index cannot be greater than polynomial order")
        else:
            return self._coeffs[index]

    def __setitem__(self, index, value):
        if index > self._order:
            return IndexError("Index cannot be greater than polynomial order")
        else:
            self._coeffs[index] = value
            return value

    def __gt__(self, other):
        return self._order > other._order

    def __add__(self, other):
        """ Performs Vector Addition of 2 Polynomials"""
        if self > other:
            result_order = self._order
            higher_order_obj = self
            lower_order_obj = other
        else:
            result_order = other._order
            higher_order_obj = other
            lower_order_obj = self
        result = Polynomial(result_order)
        for c_index, c_value in enumerate(result._coeffs):
            if c_index > lower_order_obj._order:
                result._coeffs[c_index] = higher_order_obj._coeffs[c_index]
            else:
                result._coeffs[c_index] = self._coeffs[c_index] + other._coeffs[c_index]
        return result

    def __mul__(self, other):
        """ Performs multiplication of polynomials"""
        result_order = self._order + other._order
        result = Polynomial(result_order)
        for self_idx, self_coefficient in enumerate(self._coeffs):
            for other_idx, other_coefficient in enumerate(other._coeffs):
                result[self_idx+other_idx] += self_coefficient * other_coefficient
        return result

    def d_dx(self):
        """ Performs an Analytical Derivative with Respect to X """
        D = []
        for index, coeff in enumerate(self._coeffs):
            new_row = np.zeros(self.order+1)
            if not (index+1 >= len(new_row)):
                new_row[index+1] = index+1
            D.append(new_row)
        D = np.array(D)
        result = Polynomial(self._order, np.dot(D, self._coeffs))
        return result

    def __str__(self):
        expression = f""
        for index, coefficient in enumerate(self._coeffs):
            if isinstance(coefficient, float):
                if index == 0:
                    new_term = f"{coefficient:.2f}"
                else:
                    new_term = f"{coefficient:.2f}*x^{index} + "
            if isinstance(coefficient, SymbolicVariable):
                # TODO: Finish this logic after SymbolicVariable class is complete
                if index == 0:
                    new_term = f"{coefficient:.2f}"
                else:
                    new_term = f"{coefficient:.2f}*x^{index} + "
            else:
                if index == 0:
                    new_term = f"{coefficient}"
                else:
                    new_term = f"{coefficient}*x^{index} + "
            expression = new_term + expression
        return expression




