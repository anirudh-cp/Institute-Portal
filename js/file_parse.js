const baseURL = "http://192.168.185.110:8000";

var jQueryScript = document.createElement("script");
jQueryScript.setAttribute(
  "src",
  "https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"
);
document.head.appendChild(jQueryScript);

function retrieveData(data) {
  console.log(data);
  for (let d = 0; d < data.length; d++) {
    let test = data[d];
    console.log();
    console.log(test["course_id"]);

    var t = $("#datatablesSimple").DataTable();
    t.row
      .add([
        test["course_id"],
        test["course_name"],
        test["lecture_hours"],
        test["tutorial_hours"],
        test["practical_hours"],
        test["j_project_hours"],
      ])
      .draw();
  }
}

class API {
  async getData(token) {
    const response = await fetch(baseURL + "/api/course", {
      method: "get",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    }).catch((error) => {
      // Your error is here!
      alert("Cannot connect to server. Please try again later.");
    });

    if (response.status === 200) {
      let data = await response.json();
      console.log("In API");
      console.log(data);
      // console.log("End API");
      retrieveData(data);
      return data;
    } else {
      console.log("Returning none");
      return [];
    }
  }

  async AddData(token, type, data) {
    const response = await fetch("/api/courses/", {
      method: "put",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify(data),
    }).catch((error) => {
      // Your error is here!
      console.log(error);
      alert("Cannot connect to server. Please try again later.");
    });

    if (response.status === 200) {
      return `${type} has been updated successfully!`;
    } else if (response.status === 201) {
      return `${type} has been created successfully!`;
    } else {
      let json = await response.json();
      let str = JSON.stringify(json);
      console.log(str);
      return "Error\n" + str;
    }
  }

  ExportToTable() {
    var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.xlsx|.xls)$/;
    /*Checks whether the file is a valid excel file*/
    if (regex.test($("#excelfile").val().toLowerCase())) {
      var xlsxflag = false; /*Flag for checking whether excel is .xls format or .xlsx format*/
      if ($("#excelfile").val().toLowerCase().indexOf(".xlsx") > 0) {
        xlsxflag = true;
      }
      /*Checks whether the browser supports HTML5*/
      if (typeof FileReader != "undefined") {
        var reader = new FileReader();
        reader.onload = function (e) {
          var data = e.target.result;
          /*Converts the excel data in to object*/
          if (xlsxflag) {
            var workbook = XLSX.read(data, { type: "binary" });
          } else {
            var workbook = XLS.read(data, { type: "binary" });
          }
          /*Gets all the sheetnames of excel in to a variable*/
          var sheet_name_list = workbook.SheetNames;

          var cnt = 0; /*This is used for restricting the script to consider only first sheet of excel*/
          sheet_name_list.forEach(function (y) {
            /*Iterate through all sheets*/ /*Convert the cell value to Json*/ if (
              xlsxflag
            ) {
              var exceljson = XLSX.utils.sheet_to_json(workbook.Sheets[y]);
              console.log(exceljson);
              AddData(token, type, exceljson);
            } else {
              var exceljson = XLS.utils.sheet_to_row_object_array(
                workbook.Sheets[y]
              );
            }
            if (exceljson.length > 0 && cnt == 0) {
              BindTable(exceljson, "#exceltable");
              cnt++;
            }
          });
          $("#exceltable").show();
        };
        if (xlsxflag) {
          /*If excel file is .xlsx extension than creates a Array Buffer from excel*/
          reader.readAsArrayBuffer($("#excelfile")[0].files[0]);
        } else {
          reader.readAsBinaryString($("#excelfile")[0].files[0]);
        }
      } else {
        alert("Sorry! Your browser does not support HTML5!");
      }
    } else {
      alert("Please upload a valid Excel file!");
    }
  }

  BindTable(jsondata, tableid) {
    /*Function used to convert the JSON array to Html Table*/
    var columns = BindTableHeader(
      jsondata,
      tableid
    ); /*Gets all the column headings of Excel*/
    for (var i = 0; i < jsondata.length; i++) {
      var row$ = $("<tr/>");
      for (var colIndex = 0; colIndex < columns.length; colIndex++) {
        var cellValue = jsondata[i][columns[colIndex]];
        if (cellValue == null) cellValue = "";
        row$.append($("<td/>").html(cellValue));
      }
      $(tableid).append(row$);
    }
  }
  BindTableHeader(jsondata, tableid) {
    /*Function used to get all column names from JSON and bind the html table header*/
    var columnSet = [];
    var headerTr$ = $("<tr/>");
    for (var i = 0; i < jsondata.length; i++) {
      var rowHash = jsondata[i];
      for (var key in rowHash) {
        if (rowHash.hasOwnProperty(key)) {
          if ($.inArray(key, columnSet) == -1) {
            /*Adding each unique column names to a variable array*/
            columnSet.push(key);
            headerTr$.append($("<th/>").html(key));
          }
        }
      }
    }
    $(tableid).append(headerTr$);
    return columnSet;
  }
}
