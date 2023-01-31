#import pdb
from scheme import *

statement1 = read_line("""(define outer (lambda (x y)
                          (define inner (lambda (z x) (+ x y z)))
                          inner))""")
#pdb.set_trace()
env = create_global_frame()
scheme_eval(statement1, env)
statement2 = read_line("((outer 1 2) 10 3)")
scheme_eval(statement2, env)

