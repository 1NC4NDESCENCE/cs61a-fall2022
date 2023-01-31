(define (my-filter pred s) 
  (cond ((null? s) nil)
		((pred (car s)) (cons (car s) (my-filter pred (cdr s))))
	    (else (my-filter pred (cdr s)))))


(define (interleave lst1 lst2) 
  (if (or (null? lst1) (null? lst2))
	  (if (null? lst1) lst2 lst1)
	  (cons (car lst1) (cons (car lst2) (interleave (cdr lst1) (cdr lst2))))))

(define (accumulate joiner start n term)
  (define (iter-acc joiner start num bound term)
	(if (> num bound)
		start
		(iter-acc joiner (joiner (term num) start) (+ num 1) bound term)))
  (iter-acc joiner start 1 n term))

(define (no-repeats lst) 
  (if (null? lst)
	  nil
	  (cons (car lst) (no-repeats (my-filter (lambda (x) (not (= x (car lst)))) (cdr lst))))))
