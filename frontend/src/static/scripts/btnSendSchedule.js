const inputWeekdays = document.querySelectorAll(".schedule-box"),
    btnSendSchedule = document.querySelector("#btn-send-schedule"),
    date = new Date();

const weekOfYear = (date) => {
  const startOfYear = new Date(date.getFullYear(), 0, 1);
  startOfYear.setDate(startOfYear.getDate() + (startOfYear.getDay() % 7));
  return Math.round((date - startOfYear) / (7 * 24 * 3600 * 1000));
};

const transformDateFormat = (date) => {
    return `${date.getFullYear()}-${date.getMonth() < 10 ? '0' + date.getMonth().toString(): date.getMonth()}-${date.getDate() < 10 ? '0' + date.getDate().toString(): date.getDate()}`
}

btnSendSchedule.addEventListener('click', e => {
    let scheduleObj = {
        code: localStorage.getItem('username'),
        mon: '',
        tue: '',
        wed: '',
        thu: '',
        fri: '',
        sat: '',
        sun: '',
        dt: transformDateFormat(date),
        week_num: weekOfYear(date),
        week_start_date: transformDateFormat(startOfWeek(date)),
        status: "wait"
    };
    for (let i = 0; i < inputWeekdays.length; i++) {
        scheduleObj[inputWeekdays[i].getAttribute("id")] = inputWeekdays[i].value.length === 0 ? "Day off" : inputWeekdays[i].value;
    }
    console.log(scheduleObj)
    return scheduleObj;
})

function startOfWeek(date)
{
  var diff = date.getDate() - date.getDay() + (date.getDay() === 0 ? -6 : 1);
  return new Date(date.setDate(diff));
}