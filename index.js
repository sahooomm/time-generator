const mysql = require('mysql2/promise');

// Database connection configuration
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'rootroot',
  database: 'capstone1',
};

// Queries
const query1 = "SELECT * FROM mytable";
const query2 = "SELECT * FROM mytable2";

(async () => {
  let connection;
  try {
    // Connect to the database
    connection = await mysql.createConnection(dbConfig);

    // Execute the queries and store the results
    const [cpRows] = await connection.execute(query1);
    const [fpRows] = await connection.execute(query2);

    // Fetch data for the option list
    const [result] = await connection.execute("SELECT num FROM mytable3");
    let optionList = result.map(row => parseInt(row.num));

    // Dictionary initialization
    let totalSubjectList = [];
    let totalTeacherList = [];
    let totalBatchList = new Set();
    let dayTimeslotDict = {
      mon: [1, 2, 3, 4, 5, 6],
      tue: [7, 8, 9, 10, 11, 12],
      wed: [13, 14, 15, 16, 17, 18],
      thu: [19, 20, 21, 22, 23, 24],
      fri: [25, 28, 29, 30, 31, 32],
    };
    let labAlloted = { 2: 5, 4: 7, 6: 7, 8: 6 };
    let subjectLabCredithourDict = {};
    let subjectCredithourDict = {};
    let subjectBatchDict = {};
    let noClassHoursDict = {};
    let subjectBatchIndDict = {};
    let subjectTeacherDict = {};
    let courseTypeDict = {};
    let subjectTeacherDict1 = {};

    // Function to initialize tables
    function initializeTables() {
      totalTeacherList = fpRows.map(row => row.Faculty_Name);
      totalSubjectList = cpRows.map(row => row.Course_Name);
      totalBatchList = new Set(cpRows.map(row => row.Semester));

      subjectLabCredithourDict = cpRows
        .filter(row => row.Type === 'L')
        .reduce((acc, row) => {
          acc[row.Course_Code] = row.NOCW;
          return acc;
        }, {});

      subjectCredithourDict = cpRows
        .filter(row => row.Type === 'N')
        .reduce((acc, row) => {
          acc[row.Course_Code] = row.NOCW;
          return acc;
        }, {});

      // Group courses by semester
      let groupedBySemester = cpRows.reduce((acc, row) => {
        if (!acc[row.Semester]) {
          acc[row.Semester] = [];
        }
        acc[row.Semester].push(row.Course_Code);
        return acc;
      }, {});

      subjectBatchDict = Object.keys(groupedBySemester).reduce((acc, semester) => {
        acc[semester] = [...groupedBySemester[semester], `NC${semester}`];
        return acc;
      }, {});

      noClassHoursDict = Object.keys(groupedBySemester).reduce((acc, semester) => {
        acc[`NC${semester}`] = 30 - groupedBySemester[semester].reduce((sum, code) => {
          return sum + cpRows.find(row => row.Course_Code === code).NOCW;
        }, 0);
        return acc;
      }, {});

      courseTypeDict = Object.keys(groupedBySemester).reduce((acc, semester) => {
        acc[`NC${semester}`] = 'NC';
        return acc;
      }, {});

      cpRows.forEach(row => {
        subjectBatchIndDict[row.Course_Code] = row.Semester;
        subjectTeacherDict[row.Course_Code] = row.Faculty_id;
      });

      cpRows.forEach(row => {
        subjectTeacherDict1[row.Faculty_id] = row.Course_Code;
      });

      courseTypeDict = {
        ...courseTypeDict,
        ...cpRows.reduce((acc, row) => {
          acc[row.Course_Code] = row.Type;
          return acc;
        }, {}),
      };
    }

    // Function to initialize a chromosome (schedule)
    function initializeChromosome() {
      initializeTables();
      let week = [];

      // Create an empty week (5 days, 6 time slots each day)
      for (let i = 0; i < 5; i++) {
        let day = [];
        for (let j = 0; j < 6; j++) {
          let slots = new Array(4).fill('');
          day.push(slots);
        }
        week.push(day);
      }

      // Populate the week with subjects
      week.forEach(day => {
        day.forEach(slot => {
          for (let i = 0; i < slot.length; i++) {
            let semester = (i * 2) + 2;
            let subjects = subjectBatchDict[semester] || [];

            if (subjects.length === 0) continue;

            let randomIndex = Math.floor(Math.random() * subjects.length);
            let subject = subjects[randomIndex];

            if (courseTypeDict[subject] === 'NC') {
              if (noClassHoursDict[subject] > 0) {
                slot[i] = '';
                noClassHoursDict[subject] -= 1;
                if (noClassHoursDict[subject] === 0) {
                  subjectBatchDict[semester] = subjects.filter(s => s !== subject);
                }
              }
            } else if (courseTypeDict[subject] === 'N') {
              if (subjectCredithourDict[subject] > 0) {
                slot[i] = subject;
                subjectCredithourDict[subject] -= 1;
                if (subjectCredithourDict[subject] === 0) {
                  subjectBatchDict[semester] = subjects.filter(s => s !== subject);
                }
              }
            } else if (courseTypeDict[subject] === 'L') {
              if (subjectLabCredithourDict[subject] > 0) {
                slot[i] = subject;
                subjectLabCredithourDict[subject] -= 1;
                if (subjectLabCredithourDict[subject] === 0) {
                  subjectBatchDict[semester] = subjects.filter(s => s !== subject);
                }
              }
            }
          }
        });
      });

      return week;
    }

    // Example of initializing a week (chromosome)
    const weekSchedule = initializeChromosome();
    console.log(weekSchedule);

  } catch (error) {
    console.error('Error connecting to the database:', error);
  } finally {
    if (connection) {
      await connection.end();
    }
  }
})();
