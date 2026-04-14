CREATE DATABASE IF NOT EXISTS gymdb;
USE gymdb;
show tables;

CREATE TABLE IF NOT EXISTS Member (
 member_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  age INT CHECK (age >= 15),
  gender varchar(20),
  phone VARCHAR(20) UNIQUE,
  email VARCHAR(100) UNIQUE,
  membership_type VARCHAR(50),
  membership_start DATE,
  membership_end DATE,
  trainer_id INT,
   FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id) 
);
SET foreign_key_checks = 1;


CREATE TABLE IF NOT EXISTS Trainer (
  trainer_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  specialization VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS MembershipType (
  type_id INT PRIMARY KEY AUTO_INCREMENT,
  type_name VARCHAR(50),
  duration_days INT,
  cost DECIMAL(10,2),
  benefits TEXT,
  member_id INT,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS WorkoutPlan (
  plan_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  exercise VARCHAR(200),
  sets INT,
  reps INT,
  duration INT,
  calories_burned INT,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Attendance (
  attendance_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  date DATE,
  check_in TIME,
  check_out TIME,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Progress (
  progress_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  date DATE,
  weight_kg FLOAT,
  bmi FLOAT,
  body_fat_pct FLOAT,
  goal_status VARCHAR(50),
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Payment (
  payment_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  amount DECIMAL(10,2),
  payment_date DATE,
  due_date DATE,
  status VARCHAR(50),
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Equipment (
  equipment_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  type VARCHAR(100),
  maintenance_date DATE,
  condition_status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS EquipmentUsage (
  usage_id INT PRIMARY KEY AUTO_INCREMENT,
  equipment_id INT,
  member_id INT,
  date DATE,
  duration INT,
  calories_burned INT,
  FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id),
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS DietPlan (
  diet_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  meal_type VARCHAR(50),
  calories INT,
  protein INT,
  carbs INT,
  fat INT,
  date DATE,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Class (
  class_id INT PRIMARY KEY AUTO_INCREMENT,
  trainer_id INT,
  name VARCHAR(100),
  schedule VARCHAR(100),
  duration INT,
  max_capacity INT,
  FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id) 
);

CREATE TABLE IF NOT EXISTS ClassEnrollment (
  enroll_id INT PRIMARY KEY AUTO_INCREMENT,
  class_id INT,
  member_id INT,
  enroll_date DATE,
  FOREIGN KEY (class_id) REFERENCES Class(class_id) ,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Feedback (
  feedback_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  trainer_id INT,
  rating INT,
  comments TEXT,
  date DATE,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) ,
  FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id) 
);

CREATE TABLE IF NOT EXISTS HealthCheckup (
  checkup_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  blood_pressure VARCHAR(20),
  heart_rate INT,
  sugar_level FLOAT,
  checkup_date DATE,
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

CREATE TABLE IF NOT EXISTS Notifications (
  notif_id INT PRIMARY KEY AUTO_INCREMENT,
  member_id INT,
  message TEXT,
  date DATE,
  status VARCHAR(50),
  FOREIGN KEY (member_id) REFERENCES Member(member_id) 
);

LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/members.csv"
 INTO TABLE member
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS;

LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/trainers.csv"
 INTO TABLE trainer
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS; 
 
 LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/equipment_data.csv"
 INTO TABLE Equipment
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS; 
 
 LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/payment_data.csv"
 INTO TABLE Payment
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS; 
 
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/attendance_data.csv"
 INTO TABLE attendance
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS; 
 
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/progress_data.csv"
 INTO TABLE progress
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS; 
 
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/workoutplan_data.csv"
 INTO TABLE workoutplan
 FIELDS TERMINATED BY','
 LINES TERMINATED BY'\n'
 IGNORE 1 ROWS; 
 
 
 select * from member;
 select * from trainer;
 
 SELECT name, membership_type FROM Member;

SELECT COUNT(*) AS total_members FROM Member;

SELECT name, specialization FROM Trainer;

SELECT name, membership_end FROM Member WHERE membership_end < CURDATE();

SELECT name, membership_end FROM Member
WHERE MONTH(membership_end) = MONTH(CURDATE())
AND YEAR(membership_end) = YEAR(CURDATE());

SELECT name, maintenance_date, condition_status
FROM Equipment
WHERE maintenance_date < CURDATE();


SELECT m.name, COUNT(a.attendance_id) AS total_days
FROM Attendance a
JOIN Member m ON a.member_id = m.member_id
GROUP BY m.name
ORDER BY total_days DESC
LIMIT 5;


SELECT m.membership_type, SUM(p.amount) AS total_revenue
FROM Payment p
JOIN Member m ON p.member_id = m.member_id
GROUP BY m.membership_type;

SELECT m.name, p.bmi, p.date
FROM Progress p
JOIN Member m ON p.member_id = m.member_id
WHERE p.bmi > 25;

SELECT m.name, p.amount, p.due_date
FROM Payment p
JOIN Member m ON p.member_id = m.member_id
WHERE p.status != 'Paid';

SELECT m.membership_type, AVG(p.bmi) AS avg_bmi
FROM Progress p
JOIN Member m ON p.member_id = m.member_id
GROUP BY m.membership_type;

SELECT m.name AS member_name, w.exercise, w.sets, w.reps
FROM WorkoutPlan w
JOIN Member m ON w.member_id = m.member_id;

SELECT DISTINCT m.name
FROM Member m
JOIN Attendance a ON m.member_id = a.member_id
WHERE m.member_id NOT IN (SELECT member_id FROM Payment);

SELECT DISTINCT m.name, m.membership_end, a.date AS last_attendance
FROM Member m
JOIN Attendance a ON m.member_id = a.member_id
WHERE a.date > m.membership_end;

select member_id,name,age from member where age>50;

SELECT 
    m.member_id,
    m.name,
    COUNT(a.attendance_id) 
FROM Member m 
LEFT JOIN Attendance a ON m.member_id = a.member_id
GROUP BY m.member_id, m.name;