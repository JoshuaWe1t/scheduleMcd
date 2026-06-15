const tdStatus = document.querySelectorAll('#status');

if (tdStatus) {
    for (let i = 0; i < tdStatus.length; i++) {
        let value = tdStatus[i].textContent;
        console.log();
        switch(value.toLowerCase()) {
        case 'approved':
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