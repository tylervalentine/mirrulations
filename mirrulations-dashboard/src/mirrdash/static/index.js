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
    percent = isNaN(percent) ? 0 : Math.round(percent * 10) / 10;
    document.getElementById(id+'-number').textContent = value;
    document.getElementById(id+'-circle-percentage').textContent = `${percent}%`;
    document.getElementById(id+'-circle-front').style.strokeDasharray = `${percent}, 100`;
}


const updateDashboardData = () => {
    fetch(`${BASE_URL}data`)
    .then(response => response.json())
    .then(jobInformation => {
        const {
            client1,
            client2,
            client3,
            client4,
            client5,
            client6,
            client7,
            client8,
            client9,
            client10,
            client11,
            client12,
            client13,
            client14,
            client15,
            client16,
            client17,
            clients_total,
            jobs_total,
            nginx,
            num_jobs_done, 
            num_jobs_in_progress, 
            num_jobs_waiting,
            mongo,
            redis,
            work_generator,
            work_server
        } = jobInformation;

        updateHtmlValues('jobs-waiting', num_jobs_waiting, jobs_total);
        updateHtmlValues('jobs-done', num_jobs_done, jobs_total);
        document.getElementById('total-clients-number').textContent = clients_total;
        document.getElementById('total-jobs-number').textContent = jobs_total;
        document.getElementById('client1-status').textContent = client1;
        document.getElementById('client2-status').textContent = client2;
        document.getElementById('client3-status').textContent = client3;
        document.getElementById('client4-status').textContent = client4;
        document.getElementById('client5-status').textContent = client5;
        document.getElementById('client6-status').textContent = client6;
        document.getElementById('client7-status').textContent = client7;
        document.getElementById('client8-status').textContent = client8;
        document.getElementById('client9-status').textContent = client9;
        document.getElementById('client10-status').textContent = client10;
        document.getElementById('client11-status').textContent = client11;
        document.getElementById('client12-status').textContent = client12;
        document.getElementById('client13-status').textContent = client13;
        document.getElementById('client14-status').textContent = client14;
        document.getElementById('client15-status').textContent = client15;
        document.getElementById('client16-status').textContent = client16;
        document.getElementById('client17-status').textContent = client17;
        document.getElementById('nginx-status').textContent = nginx;
        document.getElementById('mongo-status').textContent = mongo;
        document.getElementById('redis-status').textContent = redis;
        document.getElementById('work-generator-status').textContent = work_generator;
        document.getElementById('work-server-status').textContent = work_server;
    })
    .catch((err) => console.log(err));
}





