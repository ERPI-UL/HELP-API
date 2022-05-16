import API from "../script/API";
import User from "../script/User";

const TYPE = {
    BAR: "bar",
    LINE: "line"
};

/**
 * @param {Array} list list of graphs to add this graph to
 * @param {string} title graph title
 * @param {string} type graph type (line or bar)
 * @param {string[]} labels graph labels
 * @param {number[]} data graph data
 * @param {number} minBound minimum bound of the graph
 * @param {number} maxBound maximum bound of the graph
 */
function addChartToList(list, title, type, labels, data, minBound, maxBound) {
    if (minBound) data = data.concat(minBound);
    if (maxBound) data = data.concat(maxBound);
    list.push({
        title: title,
        data: {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    // label: "Data label",
                    backgroundColor: '#4F46E5',
                    borderColor: '#4F46E5',
                    data: data,
                    tension: 0.5,
                    fill: false
                }]
            }
        }
    });
}

function hideLoading() {
    document.getElementById("loadzone").style.display = "none";
}

function showLoading() {
    document.getElementById("loadzone").style.display = "block";
}

function addInfoBoxToList(list, title, info) {
    list.push({
        title: title,
        info: info
    });
}

function generateStatistics(charts, infoBoxes) {
    hideLoading();
}

function generateScenarioStatistics(graphList, InfoBoxList, scenarioID) {
    showLoading();
    API.execute_logged(API.ROUTE.STATS.SCENARIOS.AVERAGE_TIME + API.createParameters({ idScenario: scenarioID }),
        API.METHOD_GET, User.currentUser.getCredentials()
    ).then(res => {
        if (!res.data) return;
        let labels = []
        let data = []
        let total = 0;
        res.data.forEach(step => {
            if (!step.avg || !step.name) return;
            total += step.avg;
            data.push(step.avg);
            labels.push(step.name);
        });
        addChartToList(graphList, "Temps moyen par étape (seconde)", TYPE.LINE, labels, data, 0, 30);

        let nbMinutes = Math.floor(total / 60);
        let nbSeconds = total % 60;
        addInfoBoxToList(InfoBoxList, "Temps total moyen", (nbMinutes > 0 ? `${nbMinutes} minutes et ` : ``) + `${nbSeconds} secondes`);
    }).catch(console.error)
    .finally(() => {
        API.execute_logged(API.ROUTE.STATS.SCENARIOS.SKIP_RATE + API.createParameters({ idScenario: scenarioID }),
            API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
                if (!res.data) return;
                let labels = []
                let data = []
                let total = 0;
                res.data.forEach(step => {
                    if (!step.skipRate || !step.name) return;
                    if (step.skipRate == -1) step.skipRate = 0;
                    total += step.skipRate * 100;
                    data.push(Math.round(step.skipRate * 100));
                    labels.push(step.name);
                });
                addChartToList(graphList, "Taux moyen de saut d'étapes (pourcentage)", TYPE.BAR, labels, data, 0, 100);

                let moy = total / res.data.length;
                addInfoBoxToList(InfoBoxList, "Taux moyen de saut d'étapes", `${Math.round(moy)}%`);
        }).catch(console.error)
        .finally(() => {hideLoading();});
    });
}

function generateUserStatistics(charts, infoBoxes, selectedUser) {
    API.retreiveAll(API.ROUTE.STATS.USERS + selectedUser + API.ROUTE.STATS.__SESSIONS, progress => {console.log("loading progress: "+progress)}, true, 1, []).then(res => {
        addInfoBoxToList(infoBoxes, "Nombre de sessions", res.data.length);
    }).catch(err => {console.error("Error retreiving data: "+err)})
    .finally(() => {hideLoading();});
}

function generateUserScenarioStatistics(charts, infoBoxes, selectedScenario, selectedUser) {
    hideLoading();
}

export default {
    addChartToList,
    addInfoBoxToList,
    generateStatistics,
    generateUserStatistics,
    generateScenarioStatistics,
    generateUserScenarioStatistics
}