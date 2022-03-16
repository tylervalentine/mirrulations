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


const updateStatus = (container, status) => {
        let status_span = document.getElementById(container)
        if (status == "running") {
            status_span.textContent = "RUNNING";
            status_span.style.color = "green"
        }
        else {
            status_span.textContent = 'ERROR';
            status_span.style.color = "red"
        }

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
            clients_total, // TODO: is this still used?
            jobs_total,
            nginx,
            num_attachments_done, // TODO: add these in
            num_comments_done,
            num_dockets_done,
            num_documents_done,
            num_jobs_done, 
            num_jobs_in_progress, // TODO: is this still used? 
            num_jobs_waiting,
            mongo,
            redis,
            work_generator,
            work_server
        } = jobInformation;
        updateHtmlValues('jobs-waiting', num_jobs_waiting, jobs_total);
        updateHtmlValues('jobs-done', num_jobs_done, jobs_total);
        updateStatus('client1-status', client1)
        updateStatus('client2-status', client2)
        updateStatus('client3-status', client3)
        updateStatus('client4-status', client4)
        updateStatus('client5-status', client5)
        updateStatus('client6-status', client6)
        updateStatus('client7-status', client7)
        updateStatus('client8-status', client8)
        updateStatus('client9-status', client9)
        updateStatus('client10-status', client10)
        updateStatus('client11-status', client11)
        updateStatus('client12-status', client12)
        updateStatus('client13-status', client13)
        updateStatus('client14-status', client14)
        updateStatus('client15-status', client15)
        updateStatus('client16-status', client16)
        updateStatus('client17-status', client17)
        updateStatus('nginx-status', nginx)
        updateStatus('mongo-status', mongo)
        updateStatus('redis-status', redis);
        updateStatus('work-generator-status', work_generator);
        updateStatus('work-server-status', work_server);
        // Counts
        console.log("attachments: "+num_attachments_done+'\n');
        console.log("comments: "+num_comments_done+'\n');
        console.log("dockets: "+num_dockets_done+'\n');
        console.log("documents: "+num_documents_done+'\n');
        console.log("total jobs done:"+num_jobs_done+'\n');
        console.log("jobs total:"+jobs_total);
    })
    .catch((err) => console.log(err));
}





