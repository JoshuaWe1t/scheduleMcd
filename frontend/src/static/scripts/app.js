const inputTextSchedule = document.querySelectorAll(".schedule-box");

for (let i = 0; i < inputTextSchedule.length; i++) {
  inputTextSchedule[i].value = '';
}

const inputMon = document.getElementById('mon'),
 inputTue = document.getElementById('tue'),
 inputWed = document.getElementById('wed'),
 inputThu = document.getElementById('thu'),
 inputFri = document.getElementById('fri'),
 inputSat = document.getElementById('sat'),
 inputSun = document.getElementById('sun');

inputMon.addEventListener('input', e => createMask(e));
inputTue.addEventListener('input', e => createMask(e));
inputWed.addEventListener('input', e => createMask(e));
inputThu.addEventListener('input', e => createMask(e));
inputFri.addEventListener('input', e => createMask(e));
inputSat.addEventListener('input', e => createMask(e));
inputSun.addEventListener('input', e => createMask(e));

inputMon.addEventListener('change', e => validateCorrectValues(e));
inputTue.addEventListener('change', e => validateCorrectValues(e));
inputWed.addEventListener('change', e => validateCorrectValues(e));
inputThu.addEventListener('change', e => validateCorrectValues(e));
inputFri.addEventListener('change', e => validateCorrectValues(e));
inputSat.addEventListener('change', e => validateCorrectValues(e));
inputSun.addEventListener('change', e => validateCorrectValues(e));

function createMask(event) {
  const value = event.target.value.replace(/\D+/g, '');
  const formatted = value.replace(/(\d{2})(\d{2})(\d{2})(\d{2})/, '$1:$2-$3:$4');
  event.target.value = formatted;
  console.log(event.target.value)
}

function validateCorrectValues(event) {
  const value = event.target.value,
    pttrn = /^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$/gm
    pMsgError = document.getElementById("msg-error"),
    msgError = "Invalid data: Your timeshift is invalid. Please, check your data";
  
  if (pttrn.test(value) || value === '') {
    console.log(0);
    pMsgError.style.visibility = 'hidden'; 
    pMsgError.style.margin = '0';
  } else {
    console.log(1);
    pMsgError.textContent = msgError;
    pMsgError.style.visibility = 'visible';
    pMsgError.style.marginTop = "5px";
  }
}

const divforTable = document.querySelector("#tbl-schdl"),
  exm_data = [
    {'mon': 'Day off', 'tue': 'Day off', 'wed': 'Day off', 'thu': 'Day off', 'fri': 'Day off', 'sat': 'Day off', 'sun': 'Day off', 'status': 'wait', 'date': '2025-05-23'}, 
    {'mon': '16:00-00:00', 'tue': 'Day off', 'wed': '16:00-00:00', 'thu': '16:00-00:00', 'fri': 'Day off', 'sat': '08:00-00:00', 'sun': '12:00-17:00', 'status': 'wait', 'date': '2025-05-27'}, 
    {'mon': '16:00-00:00', 'tue': 'Day off', 'wed': '16:00-00:00', 'thu': '16:00-00:00', 'fri': 'Day off', 'sat': '08:00-00:00', 'sun': '12:00-17:00', 'status': 'wait', 'date': '2025-05-27'}
  ],
  ROW = exm_data.length,
  COLUMN = 9;

console.log(`row: ${ROW}, clmn: ${COLUMN}`)
//....
let table = `<table>
  <tr>
    <th class="table-clmn-title" id="mon">Mon</th>
    <th class="table-clmn-title" id="tue">Tue</th>
    <th class="table-clmn-title" id="wed">Wed</th>
    <th class="table-clmn-title" id="thu">Thu</th>
    <th class="table-clmn-title" id="fri">Fri</th>
    <th class="table-clmn-title" id="sat">Sat</th>
    <th class="table-clmn-title" id="sun">Sun</th>
    <th class="table-clmn-title" id="status">Status</th>
    <th class="table-clmn-title" id="date">Date</th>
  </tr>`,  
  match_data = {
    1: "mon",
    2: "tue",
    3: "wed",
    4: "thu",
    5: "fri",
    6: "sat",
    7: "sun",
    8: "status",
    9: "date"
  };
for (let row = 1; row <= ROW; row++) {
  tr = "<tr>";
  record = exm_data[row - 1];
  for (let clmn = 1; clmn <= COLUMN; clmn++) {
    value = record[match_data[clmn]];
    console.log(clmn, match_data[clmn], value)
    tr += `<td class="schedule" id="${match_data[clmn]}">${ucFirst(value)}</td>`;
  }
  tr += "</tr>";
  table += tr;
}
table += "</table>"
divforTable.innerHTML += table;

const tdStatus = document.querySelectorAll('#status');

if (tdStatus) {
  for (let i = 0; i < tdStatus.length; i++) {
    let value = tdStatus[i].textContent;
    console.log();
    switch(value.toLowerCase()) {
      case 'approve':
        tdStatus[i].style.color = '#39563b';
        break;
      case 'reject':
        tdStatus[i].style.color = '#723339';
        break;
      case 'wait':
        tdStatus[i].style.color = '#e98a2e';
        break;
      default:
        // code block
    } 
  }
}

function ucFirst(str) {
  if (!str) return str; // Обработка пустой строки
  return str.charAt(0).toUpperCase() + str.slice(1);
}