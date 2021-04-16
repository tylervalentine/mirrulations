'use strict';

const BASE_URL = window.location.href;

window.addEventListener('load', function init() {
    setInterval( () => {
        updateDashboardData();
    }, 5000);
})

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

        document.getElementById('jobs-waiting').textContent = num_jobs_waiting;
        document.getElementById('jobs-progress').textContent = num_jobs_in_progress;
        document.getElementById('jobs-done').textContent = num_jobs_done;
        document.getElementById('total-clients').textContent = clients_total;

    })
    .catch((err) => console.log(err));
}
