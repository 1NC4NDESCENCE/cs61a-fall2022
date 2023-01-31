(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cdr (cdr s))))

(define (ascending? asc-lst) 
  (define (helper lower asc-lst)
    (if (null? asc-lst)
		True
		(and (>= (car asc-lst) lower) (helper (car asc-lst) (cdr asc-lst)))))
  (helper 0 asc-lst))

(define (square n) (* n n))

(define (pow base exp) 
  (cond ((= exp 0) 1)
		((odd? exp) (* base (pow (* base base) (quotient exp 2))))
	    (else (pow (* base base) (/ exp 2)))))
