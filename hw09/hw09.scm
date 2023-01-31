(define-macro (when condition exprs)
			  `(if ,condition ,(cons 'begin exprs) 'okay))

(define-macro (switch expr cases)
  (cons 'cond
        (map (lambda (case)
                        (cons `(eq? ,expr ',(car case)) (cdr case)))
             cases)))

(define-macro (multi-assign sym1 sym2 expr1 expr2)
    `(begin (define ,sym1 ,expr1) (define ,sym2 ,expr2) undefined)
)

(define-macro (multi-assign sym1 sym2 expr1 expr2)
    `(begin (define res1 ,expr1) (define res2 ,expr2) (define ,sym1 res1) (define ,sym2 res2) undefined)
)

(define (replace-helper e o n)
  (if (atom? e)
      (if (eq? e o) n e)
      (cons (replace-helper (car e) o n) (replace-helper (cdr e) o n))))
(define-macro (replace expr old new)
    (replace-helper expr old new))
