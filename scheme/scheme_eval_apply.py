import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms
import scheme_builtins

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    scheme_eval( (for i '(1 2 3) (print (* i i))), global_frame_with_for_defined)
    expr.rest: (i '(1 2 3) (print (* i i)))
    evaled_args: ((quote i) (quote '(1 2 3)) (quote (print (* i i))))
    scheme_apply(for, evaled_args, env)
    make_child_frame(for.formals, evaled_args)
    formal = (quote i)

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        procedure = scheme_eval(expr.first, env)
        if not issubclass(type(procedure), Procedure):
            raise SchemeError('uncallable')
        if isinstance(procedure, MacroProcedure):
            # evaled_args = expr.rest.map(lambda arg: Pair('quote', Pair(arg, nil)))
            return scheme_apply(procedure, expr.rest, env)
        else:
            evaled_args = expr.rest.map(lambda arg: scheme_eval(arg, env))
            return scheme_apply(procedure, evaled_args, env)
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        arg_lst = []
        while args is not nil:
            arg_lst.append(args.first)
            args = args.rest
        if procedure.need_env:
            arg_lst.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            return procedure.py_func(*arg_lst)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        new_env = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        new_env = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)
        # END PROBLEM 11
    elif isinstance(procedure, MacroProcedure):
        new_env = procedure.env.make_child_frame(procedure.formals, args)
        return scheme_eval(scheme_eval(procedure.body, new_env), env)
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    res = None
    while expressions:
        res = scheme_eval(expressions.first, env, expressions.rest is nil)
        expressions = expressions.rest
    return res
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env)
        return result
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)
