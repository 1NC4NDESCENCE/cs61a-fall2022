(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 15
;; Returns a list of two-element lists
(define (enumerate s)
  (define (helper lst index)
		(if (null? lst)
			nil
			(cons (list index (car lst)) (helper (cdr lst) (+ index 1)))))
  (helper s 0))

;; Problem 16

;; Merge two lists LIST1 and LIST2 according to ORDERED? and return
;; the merged lists.
(define (merge ordered? list1 list2)
  ; BEGIN PROBLEM 16
  (if (or (null? list1) (null? list2))
	  (if (null? list1)
		  list2
		  list1)
	  (if (ordered? (car list1) (car list2))
		  (cons (car list1) (cons (car list2) (merge ordered? (cdr list1) (cdr list2))))
		  (cons (car list2) (cons (car list1) (merge ordered? (cdr list1) (cdr list2))))))
  )
  ; END PROBLEM 16

;; Optional Problem 2

;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN OPTIONAL PROBLEM 2
				 expr
         ; END OPTIONAL PROBLEM 2
         )
				((quoted? expr)
         ; BEGIN OPTIONAL PROBLEM 2
				 expr
         ; END OPTIONAL PROBLEM 2
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
					 (cons form (cons (map let-to-lambda params) (map let-to-lambda body)))
           ; END OPTIONAL PROBLEM 2
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
					 (define formals_and_args (zip values))
					 (let ((formals (car formals_and_args))
								 (values (map let-to-lambda (cadr formals_and_args))))
						 (cons (cons 'lambda (cons formals (map let-to-lambda body))) values))
           ; END OPTIONAL PROBLEM 2
           ))
        (else
         ; BEGIN OPTIONAL PROBLEM 2
				 (map let-to-lambda expr)
         ; END OPTIONAL PROBLEM 2
         )))

; Some utility functions that you may find useful to implement for let-to-lambda

(define (zip pairs)
	(define pairs (reverse pairs))
	(define (helper lst res)
		(if (null? lst)
			res
			(let ((pair (car lst)))
				(helper (cdr lst) (list (cons (car pair) (car res)) (cons (cadr pair) (cadr res)))))))
	(helper pairs '(() ())))

(define (map f lst)
  (if (null? lst)
	  nil
	  (cons (f (car lst)) (map f (cdr lst)))))

(define (nondecreaselist s)
	(define s (reverse s))
	(define (helper lst result)
		(cond ((eq? lst nil) (cons result nil)) 
					((< (car result) (car lst)) (cons result (helper (cdr lst) (cons (car lst) nil))))
					(else (helper (cdr lst) (cons (car lst) result)))))
	(reverse (helper (cdr s) (cons (car s) nil))))

(define (reverse lst)
  (define (helper lst res)
	  (if (null? lst)
		  res
			(helper (cdr lst) (cons (car lst) res))))
	(helper lst nil))

(define (make-or expr1 expr2)
  `(let ((res (eval ,expr1)))
		 (if res res ,expr2)))

(define (make-make-or)
	'(define (make-or expr1 expr2)
		`(let ((res (eval ,expr1)))
			 (if res res ,expr2))))

(define (make-long-or args)
	(if (eq? args nil) 
			#f
			(let ((res (eval (car args)))
						(rest (cdr args)))
				`(if ,res
						 ,res
						 (eval (make-long-or ',rest))))))

