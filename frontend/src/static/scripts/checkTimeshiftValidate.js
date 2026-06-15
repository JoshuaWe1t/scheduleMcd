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
    const 
        value = event.target.value.replace(/\D+/g, ''),
        formatted = value.replace(/(\d{2})(\d{2})(\d{2})(\d{2})/, '$1:$2-$3:$4');
    event.target.value = formatted;
    console.log(event.target.value)
}

function validateCorrectValues(event) {
const 
    input = event.target;
    value = event.target.value,
    pttrn = /^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$/gm
    pMsgError = document.getElementById("msg-error"),
    msgError = "Invalid data: Your timeshift is invalid. Please, check your data";

    if (pttrn.test(value) || value === '') {
        pMsgError.style.visibility = 'hidden'; 
        pMsgError.style.margin = '0';
        input.style.borderColor = "#39563b";
    } else {
        pMsgError.textContent = msgError;
        pMsgError.style.visibility = 'visible';
        pMsgError.style.marginTop = "5px";
        input.style.borderColor = '#e98a2e';
    }
}