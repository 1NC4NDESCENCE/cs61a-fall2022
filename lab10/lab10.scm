(define (over-or-under num1 num2) 
  (cond ((< num1 num2) -1)
		((> num1 num2) 1)
		(else 0)))

(define (make-adder num) 
  (lambda (x) (+ x num)))

(define (composed f g) 
  (lambda (x) (f (g x))))

(define lst 
  (let ((a (list 1)) 
		(b (list 3 4)))
	(list a 2 b 5)))

(define (duplicate lst) 
  (if (null? lst)
	  nil
	  (cons (car lst) (cons (car lst) (duplicate (cdr lst))))))
