#!/usr/bin/env sbcl --script

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; input/output management
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Function to read input from standard input
(defun read-input ()
  "Reads an S-expression from the standard input."
  (read))

;;; Converts an association list into a JSON string
(defun alist-to-json (alist)
  "Converts an association list to a JSON string."
  (let ((json "{"))
    (loop for (key . value) in alist
          for keystr = (if (symbolp key)
                           (symbol-name key)
                           (princ-to-string key))
          for valuestr = (cond
                          ((stringp value) (format nil "\"~a\"" value))
                          ((numberp value) (princ-to-string value))
                          ((null value) "null")
                          ((eq value t) "true")
                          (t (format nil "\"~a\"" value)))
          do (progn
               (when (> (length json) 1)
                 (setf json (concatenate 'string json ", ")))
               (setf json (concatenate 'string json
                                        "\"" keystr "\": " valuestr))))
    (concatenate 'string json "}")))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; utility functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Retrieves the title of a movie from an alist
(defun movie-title (movie)
  "Extracts the title from a movie association list."
  (cdr (assoc :title movie)))

;;; Function to get movies from input's car
(defun get-movies (input)
  "Extracts the list of movies from the car of the input."
  (car input))

;;; Function to get user data from input's cdr
(defun get-user (input)
  "Extracts user information from the cdr of the input."
  (cdr input))

;;; Retrieves a specific piece of information about the user
(defun get-user-info (user key)
  "Gets a specific piece of information (key) about the user."
  (cdr (assoc key user)))

;;; Retrieves the genres of a movie
(defun get-movie-genres (movie)
  "Gets the genres of a movie."
  (get-movie-info movie :genre_ids))

;;; Retrieves a specific field from a movie
(defun get-movie-info (movie key)
  "Gets a specific field (key) from a movie."
  (cdr (assoc key movie)))

;;; Retrieves the user's favorite movies
(defun get-user-favorite-movies (user)
  "Gets the user's list of favorite movies."
  (get-user-info user :movies))

;;; Retrieves the user's mood-based movies
(defun get-user-mood-movies (user)
  "Gets the user's mood-based movie list."
  (get-user-info user :mood_movies))

;;; Returns a list of titles of the user's favorite movies
(defun get-user-fav-movie-titles (user)
  "Returns a list of titles of the user's favorite movies."
  (mapcar #'movie-title (get-user-favorite-movies user)))

;;; Returns a list of titles of the user's mood-based movies
(defun get-user-mood-movies-titles (user)
  "Returns a list of titles of the user's mood-based movies."
  (mapcar #'movie-title (get-user-mood-movies user)))

;;; Retrieves the vote average of a movie
(defun movie-vote-average (movie)
  "Extracts the vote average (vote_average) of a movie."
  (cdr (assoc :vote_average movie)))

(defun get-user-age (user)
  "Gets the user's age."
  (get-user-info user :age))

;;; Checks if a movie is for adults
(defun is-movie-adult (movie)
  "Checks if a movie is marked as adult-only."
  (get-movie-info movie :adult))

;; Function to get the popularity of a movie
(defun get-movie-popularity (movie)
  "Gets the popularity of a movie."
  (get-movie-info movie :popularity))

;;; Retrieves the original language of a movie
(defun get-movie-original-language (movie)
  "Gets the original language of a movie."
  (get-movie-info movie :original_language))

;;; Function to retrieve the release year of a movie
(defun get-movie-year (movie)
  "Extracts the release year from a movie's release date."
  (let ((release-date (get-movie-info movie :release_date)))
    (if (and release-date (>= (length release-date) 4))
        (parse-integer (subseq release-date 0 4)) ; Extract the first 4 characters (year)
        nil))) ; Return nil if release date is not available or too short

(defun get-movie-id (movie)
  "Gets the ID of a movie."
  (cdr (assoc :id movie)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Scoring functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Function to calculate the percentage similarity between a movie's genre IDs and the user's favorite movie genres
(defun calculate-genre-similarity (movie movies)
  "Calculates the percentage similarity between a movie's genre IDs and the genre IDs of the user's favorite movies."
  (let* ((movie-genres (get-movie-genres movie))
         (favorite-genres (remove-duplicates (apply #'append (mapcar #'get-movie-genres movies)) :test #'equal))
         (common-genres (intersection movie-genres favorite-genres :test #'equal))
         (total-genres (length movie-genres)))
    (if (> total-genres 0)
        (* 100 (/ (float (length common-genres)) total-genres)) ; Percentage similarity
        0.0))) ; Return 0 if the movie has no genres

;;; Function to calculate the year difference between two movies
(defun calculate-year-difference (movie1 movie2)
  "Calculates the absolute year difference between two movies."
  (let ((year1 (get-movie-year movie1))
        (year2 (get-movie-year movie2)))
    (if (and year1 year2)
        (abs (- year1 year2)) ; Calculate absolute difference
        nil))) ; Return nil if either year is unavailable

;;; Function to calculate language similarity
(defun calculate-language-similarity (movie user-mood-movies user-favorite-movies)
  ;; on compte le nombre de fois que le language du film apparait dans les films favoris et mood et on divise par le nombre de films total dans les deux listes
  "Calculates the language similarity between a movie and the user's favorite and mood-based movies."
  (let* ((movie-language (get-movie-original-language movie))
         (user-mood-languages (mapcar #'get-movie-original-language user-mood-movies))
         (user-favorite-languages (mapcar #'get-movie-original-language user-favorite-movies))
         (total-movies (+ (length user-mood-languages) (length user-favorite-languages)))
         (common-languages (+ (count movie-language user-mood-languages :test #'string=)
                              (count movie-language user-favorite-languages :test #'string=))))
    (if (> total-movies 0)
        (* (/ (float common-languages) total-movies) 100) ; Language similarity in percentage
        0.0))) ; Return 0 if there are no movies to compare

(defun score-movie (movie user)
  "Scores a movie based on multiple criteria."
  (let* ((user-favorites (get-user-favorite-movies user))
         (user-mood (get-user-mood-movies user))
         (year-difference (if user-mood
                              (let ((average-year (/ (reduce #'+ (mapcar #'get-movie-year user-mood)) 
                                                     (length user-mood))))
                                (if (get-movie-year movie)
                                    (abs (- (get-movie-year movie) average-year))
                                    nil))
                              nil))
         (genre-similarity-mood (calculate-genre-similarity movie user-mood))
         (genre-similarity-favorites (calculate-genre-similarity movie user-favorites))
         (popularity-score (/ (get-movie-popularity movie) 100.0))
         (vote-score (* (movie-vote-average movie) 10))
         (language-similarity (calculate-language-similarity movie user-mood user-favorites)))
    (- (+ (* 0.3 genre-similarity-mood)
          (* 0.25 genre-similarity-favorites)
          (* 0.15 popularity-score)
          (* 0.25 vote-score)
          (* 0.15 language-similarity))
       (* 0.1 (if year-difference
                  (min 1.0 (/ year-difference 100.0))
                  0.0)))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; recommendation functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

  
(defun recommend-movies (db user &optional (n 5))
  "Recommends the top N movies by a calculated score from the top 50 of the database 
  that are not in the user's favorites or mood-movies. Filters adult movies if the user is under 18.
  Ensures no duplicate IDs in the final list."
  (let* ((user-fav-titles (get-user-fav-movie-titles user))
         (user-mood-titles (get-user-mood-movies-titles user))
         ;; Filtrage initial des films non admissibles
         (filtered-db (remove-if (lambda (movie)
                                   (or (and (< (get-user-age user) 18) (is-movie-adult movie))
                                       (member (movie-title movie) user-fav-titles :test #'string=)
                                       (member (movie-title movie) user-mood-titles :test #'string=)))
                                 db)))
    ;; Tri des films par score décroissant
    (setf filtered-db (sort filtered-db #'> :key (lambda (movie) (score-movie movie user))))
    ;; Prendre les 50 premiers films triés
    (let ((top-50 (subseq filtered-db 0 (min 50 (length filtered-db))))
          (unique-ids '())
          (unique-movies '()))
      ;; Supprimer les duplicatas dans les 50 premiers
      (dolist (movie top-50)
        (let ((id (get-movie-id movie)))
          (unless (member id unique-ids)
            (push id unique-ids)
            (push movie unique-movies))))
      ;; Retourner les N premiers films sans duplicatas
      (subseq (reverse unique-movies) 0 (min n (length unique-movies))))))



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main function
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Main function to process input and generate recommendations
(defun main ()
  "Main function: reads input, generates recommendations, and outputs them as JSON."
  (let* ((input (read-input))
         (db (get-movies input))
         (user (get-user input))
         (recommendations (recommend-movies db user)))
    ;; Convert recommendations to JSON
    (let ((json "["))
      (loop for movie in recommendations
            for i from 0 do
              (when (> i 0)
                (setf json (concatenate 'string json ", ")))
              (setf json (concatenate 'string json (alist-to-json movie))))
      (setf json (concatenate 'string json "]"))
      (print json))))

(main)
