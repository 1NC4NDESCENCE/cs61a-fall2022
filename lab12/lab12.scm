(define-macro
  (if-macro condition if-true if-false)
	`(if ,condition ,if-true ,if-false))

(define-macro (or-macro expr1 expr2)
  `(let ((v1 ,expr1))
     (if v1
         v1
         ,expr2)))

(define (replicate x n) 
	(define (helper n res)
		(if (= n 0) res (helper (- n 1) (cons x res))))
	(helper n nil))

(define-macro (repeat-n expr n) 
							`(if (!= ,n 0)
									 (begin ,expr (repeat-n ,expr (- ,n 1)))))

(define (!= expr1 expr2)
	(not (= expr1 expr2)))

;(define-macro (!= expr1 expr2)
;							`(not (= ,expr1 ,expr2)))

(define
 (list-of map-expr for var in lst if filter-expr)
 `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst)))

(define-macro (list-of-macro map-expr
                             for
                             var
                             in
                             lst
                             if
                             filter-expr)
  `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst)))
