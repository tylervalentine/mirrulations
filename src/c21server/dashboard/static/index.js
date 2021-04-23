'use strict';

const BASE_URL = window.location.href;
const RADIUS = 80;
const NUMBER_ANIMATION_STEP = 4;

window.addEventListener('load', function init() {
    updateDashboardData();
    setInterval(updateDashboardData, 5000);
})

const updateHtmlValues = (id, value, total) => {
    let percent = (value/total) * 100;
    percent = isNaN(percent) ? 0 : percent
    document.getElementById(id+'-number').textContent = value;
    document.getElementById(id+'-circle-percentage').textContent = `${percent}%`;
    document.getElementById(id+'-circle-front').style.strokeDasharray = `${percent}, 100`;
}

const updateDashboardData = () => {
    fetch(`${BASE_URL}data`)
    .then(response => response.json())
    .then(jobInformation => {
        const { 
            clients_total, 
            jobs_total, 
            num_jobs_done, 
            num_jobs_in_progress, 
            num_jobs_waiting 
        } = jobInformation;

        updateHtmlValues('jobs-waiting', num_jobs_waiting, jobs_total);
        updateHtmlValues('jobs-progress', num_jobs_in_progress, jobs_total);
        updateHtmlValues('jobs-done', num_jobs_done, jobs_total);
        document.getElementById('total-clients-number').textContent = clients_total;
    })
    .catch((err) => console.log(err));
}





