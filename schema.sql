DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results;

CREATE TABLE students(
StudentID INTEGER PRIMARY KEY,
StudentFirstName VARCHAR NOT NULL,
StudentLastName VARCHAR NOT NULL);

CREATE TABLE quizzes(
QuizID INTEGER PRIMARY KEY,
QuizSubject VARCHAR NOT NULL,
QuizQuestions INTEGER NOT NULL,
QuizDate VARCHAR NOT NULL);

CREATE TABLE results(
StudentID INTEGER NOT NULL,
QuizID INTEGER NOT NULL,
Score INTEGER NOT NULL);