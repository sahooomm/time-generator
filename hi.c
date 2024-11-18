#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql/mysql.h>
#include <time.h>

#define MAX_SUBJECTS 100
#define MAX_TEACHERS 100
#define MAX_BATCHES 10
#define MAX_SLOTS 4
#define DAYS_IN_WEEK 5
#define SLOTS_IN_DAY 6

// MySQL connection config
const char *DB_USER = "root";
const char *DB_PASS = "rootroot";
const char *DB_HOST = "localhost";
const char *DB_NAME = "capstone1";

// Global variables
char total_subject_list[MAX_SUBJECTS][50];
char total_teacher_list[MAX_TEACHERS][50];
int total_batch_list[MAX_BATCHES];
int total_batch_count = 0;

int subject_lab_credithour_dict[MAX_SUBJECTS];
int subject_credithour_dict[MAX_SUBJECTS];
char subject_batch_dict[MAX_BATCHES][MAX_SUBJECTS][50];
int subject_batch_count[MAX_BATCHES];
int no_class_hours_dict[MAX_BATCHES];
char course_type_dict[MAX_SUBJECTS][3];
int subject_batch_ind_dict[MAX_SUBJECTS];
int subject_teacher_dict[MAX_SUBJECTS];

// Function prototypes
void initializeTables(MYSQL *conn);
void initializeChromosome(char week[DAYS_IN_WEEK][SLOTS_IN_DAY][MAX_SLOTS][50]);
void printWeek(char week[DAYS_IN_WEEK][SLOTS_IN_DAY][MAX_SLOTS][50]);

int main() {
    // Connect to MySQL
    MYSQL *conn = mysql_init(NULL);
    if (conn == NULL) {
        fprintf(stderr, "mysql_init() failed\n");
        return EXIT_FAILURE;
    }
    if (mysql_real_connect(conn, DB_HOST, DB_USER, DB_PASS, DB_NAME, 0, NULL, 0) == NULL) {
        fprintf(stderr, "mysql_real_connect() failed\n");
        mysql_close(conn);
        return EXIT_FAILURE;
    }

    // Initialize population
    int popz = 100;
    char population[popz][DAYS_IN_WEEK][SLOTS_IN_DAY][MAX_SLOTS][50];

    for (int i = 0; i < popz; ++i) {
        initializeChromosome(population[i]);
    }

    // Print the first chromosome
    printWeek(population[0]);

    // Clean up
    mysql_close(conn);
    return EXIT_SUCCESS;
}

void initializeTables(MYSQL *conn) {
    // Fetch teachers
    if (mysql_query(conn, "SELECT Faculty_Name FROM mytable2")) {
        fprintf(stderr, "%s\n", mysql_error(conn));
        exit(EXIT_FAILURE);
    }
    MYSQL_RES *res = mysql_store_result(conn);
    int teacher_count = 0;
    while (MYSQL_ROW row = mysql_fetch_row(res)) {
        strcpy(total_teacher_list[teacher_count++], row[0]);
    }
    mysql_free_result(res);

    // Fetch subjects
    if (mysql_query(conn, "SELECT Course_Name, Course_Code, Type, Semester, NOCW FROM mytable")) {
        fprintf(stderr, "%s\n", mysql_error(conn));
        exit(EXIT_FAILURE);
    }
    res = mysql_store_result(conn);
    int subject_count = 0;

    while (MYSQL_ROW row = mysql_fetch_row(res)) {
        strcpy(total_subject_list[subject_count], row[0]);
        int semester = atoi(row[3]);
        total_batch_list[total_batch_count++] = semester;

        if (strcmp(row[2], "L") == 0) {
            subject_lab_credithour_dict[subject_count] = atoi(row[4]);
        } else if (strcmp(row[2], "N") == 0) {
            subject_credithour_dict[subject_count] = atoi(row[4]);
        }

        strcpy(subject_batch_dict[semester][subject_count], row[1]);
        subject_batch_count[semester]++;
        subject_teacher_dict[subject_count] = atoi(row[5]); // Assuming Faculty_id is in row[5]
        subject_batch_ind_dict[subject_count] = semester;
        strcpy(course_type_dict[subject_count], row[2]);
        subject_count++;
    }
    mysql_free_result(res);

    // Initialize no_class_hours_dict
    for (int i = 0; i < total_batch_count; i++) {
        no_class_hours_dict[i] = 30; // Placeholder; this should be calculated based on courses
    }
}

void initializeChromosome(char week[DAYS_IN_WEEK][SLOTS_IN_DAY][MAX_SLOTS][50]) {
    initializeTables(conn); // Assuming conn is passed as a parameter in a complete code
    for (int i = 0; i < DAYS_IN_WEEK; ++i) {
        for (int j = 0; j < SLOTS_IN_DAY; ++j) {
            for (int k = 0; k < MAX_SLOTS; ++k) {
                strcpy(week[i][j][k], ""); // Initialize slots
            }
        }
    }

    // Populate the week with random subjects
    for (int i = 0; i < DAYS_IN_WEEK; ++i) {
        for (int j = 0; j < SLOTS_IN_DAY; ++j) {
            for (int k = 0; k < MAX_SLOTS; ++k) {
                int random_index = rand() % subject_batch_count[(j * 2) + 2];
                char *sub = subject_batch_dict[(j * 2) + 2][random_index];

                // Check course type and update accordingly
                if (strcmp(course_type_dict[random_index], "NC") == 0) {
                    if (no_class_hours_dict[random_index] > 0) {
                        strcpy(week[i][j][k], "");
                        no_class_hours_dict[random_index]--;
                    }
                } else if (strcmp(course_type_dict[random_index], "N") == 0) {
                    if (subject_credithour_dict[random_index] > 0) {
                        strcpy(week[i][j][k], sub);
                        subject_credithour_dict[random_index]--;
                    }
                } else if (strcmp(course_type_dict[random_index], "L") == 0) {
                    if (subject_lab_credithour_dict[random_index] > 0) {
                        strcpy(week[i][j][k], sub);
                        subject_lab_credithour_dict[random_index]--;
                    }
                }
            }
        }
    }
}

void printWeek(char week[DAYS_IN_WEEK][SLOTS_IN_DAY][MAX_SLOTS][50]) {
    for (int i = 0; i < DAYS_IN_WEEK; ++i) {
        for (int j = 0; j < SLOTS_IN_DAY; ++j) {
            for (int k = 0; k < MAX_SLOTS; ++k) {
                printf("%s ", week[i][j][k]);
            }
            printf("\n");
        }
        printf("\n");
    }
}
