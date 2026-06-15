// Получаем все кнопки + (параграфы)
const divInfoBox = document.querySelector("#info-box"),
    data = [
    {'code_emploeey': '400000', 'first_name': 'Nick', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}, 
    {'code_emploeey': '600000', 'first_name': 'Nil4', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}, 
    {'code_emploeey': '400000', 'first_name': 'Nick', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}, 
    {'code_emploeey': '300000', 'first_name': 'Nil1', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}
];

for (let i = 0; i < data.length; i++) {
    divInfoBox.innerHTML += `
    <div class="row-info" style="height: auto; overflow: visible;">
        <p class="expandBtn" id="user-${data[i].code_emploeey}">+</p>
        <div class="info-elm" id="employee">
            <p>${data[i].code_emploeey} ${data[i].first_name}</p>
            <p>0 Day off</p>
        </div>
        <div class="info-elm" id="cntrl-btn">
            <button class="approve-btn">Approve</button>
            <button class="reject-btn">Reject</button>
        </div>
    </div>`
}

function createTable(data, code) {
    let result = data.find(employee => employee.code_emploeey === code);
    console.log(result)
    table = `
        <tr>
            <th>Mon</th>
            <th>Tue</th>
            <th>Wed</th>
            <th>Thu</th>
            <th>Fri</th>
            <th>Sat</th>
            <th>Sun</th>
            <th>Week</th>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">${result.mon}</td>
            <td style="text-align: center; vertical-align: middle;">${result.tue}</td>
            <td style="text-align: center; vertical-align: middle;">${result.wed}</td>
            <td style="text-align: center; vertical-align: middle;">${result.thu}</td>
            <td style="text-align: center; vertical-align: middle;">${result.fri}</td>
            <td style="text-align: center; vertical-align: middle;">${result.sat}</td>
            <td style="text-align: center; vertical-align: middle;">${result.sun}</td>
            <td style="text-align: center; vertical-align: middle;">${result.week_start_date}</td>
        </tr>
    `;
    return table;
}

const expandButtons = document.querySelectorAll('.expandBtn');

expandButtons.forEach(button => {
    const parent = button.closest('.row-info');
    parent.dataset.originalHeight = parent.style.height || parent.offsetHeight + 'px';
    
    button.addEventListener('click', e => {
        const existingTable = parent.querySelector('table'),
            userCode = (button.id).substring(5);
        if (existingTable) {
            // Скрываем таблицу и возвращаем высоту
            existingTable.remove();
            parent.style.height = parent.dataset.originalHeight;
            parent.style.overflow = 'hidden';
            button.textContent = '+'; // меняем знак обратно
        } else {
            // Показываем таблицу и расширяем блок
            parent.style.height = 'auto';
            parent.style.overflow = 'visible';

            const table = document.createElement('table');
            table.id = "tbl-" + button.id;
            table.border = '1';
            table.style.width = '100%';
            table.innerHTML += createTable(data, userCode);

            parent.appendChild(table);
            button.textContent = '−'; // меняем знак на минус
        }
    })
})