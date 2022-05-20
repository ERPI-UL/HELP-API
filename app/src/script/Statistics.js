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
function addChartToList(list, title, type, labels, sets) {

    const colors = [
        ['#4F46E540', '#4F46E5'],
        ['#0004', '#000']
    ]

    let acc = 0;
    list.push({
        title: title,
        data: {
            type: type,
            data: {
                labels: labels,
                datasets: sets.map(set => {
                    return {
                        label: set.label,
                        backgroundColor: colors[acc][0],
                        borderColor: colors[acc++][1],
                        data: set.data,
                        tension: 0.5,
                        fill: true,
                        hidden: acc > 1
                    }
                })
            }
        }
    });
}

function hideLoading() {
    document.getElementById("loadzone").style.display = "none";
}

function showLoading(...lists) {
    lists.forEach(l => l.splice(0, l.length));
    window.indico.refreshStatistics();
    document.getElementById("loadzone").style.display = "block";
    document.getElementById("nodatazone").style.display = "none";
}

function stringTime(time) {
    let nbMinutes = Math.floor(time / 60);
    let nbSeconds = time % 60;
    return (nbMinutes > 0 ? `${Math.round(nbMinutes)} minute${nbMinutes >= 2 ? "s" : ""} et ` : ``) + `${Math.round(nbSeconds)} seconde${nbSeconds >= 2 ? "s" : ""}`
}

function addInfoBoxToList(list, title, info) {
    list.push({
        title: title,
        infos: info
    });
}

function generateStatistics(charts, infoBoxes) {
    showLoading(charts, infoBoxes);
    return new Promise((resolve, reject) => {
        API.execute_logged(API.ROUTE.USERS + API.createPagination(1, 1), API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
            addInfoBoxToList(infoBoxes, "Nombre d'utilisateurs", res.total);
        }).catch(reject).finally(() => {
            API.execute_logged(API.ROUTE.SCENARIOS + API.createPagination(1, 1), API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
                addInfoBoxToList(infoBoxes, "Nombre de scénarios", res.total);
            }).catch(reject).finally(() => {
                API.retreiveAll(API.ROUTE.SCENARIOS).then(res => {
                    let scenarioTimes = [];
                    let retreiveCounter = 0;
                    const checkForEnd = () => {
                        if (++retreiveCounter == res.length) {
                            let avg = scenarioTimes.reduce((a, b) => a + b) / scenarioTimes.length;
                            addInfoBoxToList(infoBoxes, "Temps moyen des scénarios", stringTime(avg));
                            hideLoading();
                            resolve();
                        }
                    }
                    res.forEach(scenario => {
                        API.execute_logged(API.ROUTE.STATS.SCENARIOS.AVERAGE_TIME + API.createParameters({ idScenario: scenario.id }), API.METHOD_GET, User.currentUser.getCredentials()).then(res2 => {
                            if (!res2.data) return;
                            let labels = [];
                            let data = [];
                            let total = 0;
                            res2.data.forEach(step => {
                                if (step.avg === undefined || step.name === undefined) return;
                                total += step.avg;
                                data.push(step.avg);
                                labels.push(step.name);
                            });
                            scenarioTimes.push(total);
                            checkForEnd();
                        });
                    });
                });
            });
        });
    });
}

function generateScenarioStatistics(graphList, InfoBoxList, scenarioID) {
    showLoading(graphList, InfoBoxList);
    return new Promise((resolve, reject) => {
        let scenario = null;
        API.execute_logged(API.ROUTE.SCENARIOS+scenarioID, API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
            scenario = res;
            scenario.labels = scenario.steps.map(s => s.name);
        }).catch(reject).finally(() => {
            API.execute_logged(API.ROUTE.STATS.SCENARIOS.AVERAGE_TIME + API.createParameters({ idScenario: scenarioID }), API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
                if (!res.data) return;
                let data = [];
                let total = 0;
                res.data.forEach(step => {
                    total += step.avg;
                    data.push(step.avg);
                });
                let accumulator = 0;
                addChartToList(graphList, "Temps moyen par étape (s)", TYPE.LINE, scenario.labels, [
                    { label: "temps moyen", data: data},
                    { label: "temps absolu", data: data.map(d => accumulator+=d)}
                ]);
                addInfoBoxToList(InfoBoxList, "Temps total moyen", stringTime(total));
            }).catch(reject).finally(() => {
                API.execute_logged(API.ROUTE.STATS.SCENARIOS.SKIP_RATE + API.createParameters({ idScenario: scenarioID }), API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
                    if (!res.data) return;
                    let labels = [];
                    let data = [];
                    let total = 0;
                    res.data.forEach(step => {
                        if (step.skipRate === undefined || step.name === undefined) return;
                        if (step.skipRate == -1) step.skipRate = 0;
                        total += step.skipRate * 100;
                        data.push(Math.round(step.skipRate * 100));
                        labels.push(step.name);
                    });
                    addChartToList(graphList, "Taux moyen de saut d'étapes (%)", TYPE.BAR, labels, [{ label: "Taux relatif", data: data }]);

                    let moy = total / res.data.length;
                    addInfoBoxToList(InfoBoxList, "Taux moyen de saut d'étape", `${Math.round(moy)}%`);
                }).catch(reject).finally(() => {
                    API.execute_logged(API.ROUTE.STATS.SCENARIOS.PERFORM_RATE+API.createParameters({idScenario: scenarioID}), API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
                        if (!res.data) return;
                        let labels = [];
                        let data = [];
                        let total = 0;
                        console.log(res.data.map(s => s.performRate))
                        res.data.forEach(step => {
                            total += step.performRate*100;
                            data.push(step.performRate*100);
                            labels.push(step.name);
                        });
                        console.log(labels);
                        addChartToList(graphList, "Taux moyen d'exécution (%)", TYPE.BAR, labels, [{ label: "Taux relatif", data: data }]);
                        addInfoBoxToList(InfoBoxList, "Taux moyen d'exécution", `${Math.round(total / res.data.length)}%`);
                        hideLoading();
                        resolve();
                    });
                });
            });
        });
    });
}

function generateUserStatistics(charts, infoBoxes, selectedUser) {
    showLoading(charts, infoBoxes);
    return new Promise((resolve, reject) => {
        API.retreiveAll(API.ROUTE.STATS.USERS + selectedUser + API.ROUTE.STATS.__SESSIONS, progress => { console.log("loading progress: " + progress) }, true, 1, []).then(res => {
            let scenarios = []
            res.forEach(session => {
                if (!(session.idScenario in scenarios))
                    scenarios.push(session.idScenario);
            });
            addInfoBoxToList(infoBoxes, "Nombre de sessions", res.length);
            addInfoBoxToList(infoBoxes, "Nombre de scénarios", scenarios.length);
            resolve();
        }).catch(reject).finally(() => { hideLoading(); });
    });
}

function generateUserScenarioStatistics(charts, infoBoxes, selectedScenario, selectedUser) {
    showLoading(charts, infoBoxes);
    return new Promise((resolve, reject) => {
        let scenario = null;
        API.execute_logged(API.ROUTE.SCENARIOS + selectedScenario, API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
            scenario = res;
        }).finally(() => {
            API.retreiveAll(API.ROUTE.STATS.USERS + selectedUser + API.ROUTE.STATS.__SESSIONS + API.createParameters({ id_scenario: selectedScenario })).then(res => {
                let sessions = [];
                let retreiveCounter = 0;

                res.forEach(session => {
                    API.execute_logged(API.ROUTE.STATS.SESSIONS + session.id, API.METHOD_GET, User.currentUser.getCredentials()).then(res2 => {
                        let labels = [];
                        let data = [];
                        sessions.push(res2);
                        res2.playedSteps.forEach(step => {
                            if (step.time === undefined || step.step_id === undefined) return;
                            data.push(step.time);
                            labels.push({ name: scenario.steps.find(s => s.id === step.step_id).name, order: step.progressNumber });
                        });
                        checkForEnd();
                    }).catch(console.error);
                })
                const checkForEnd = () => {
                    if (++retreiveCounter == res.length) {
                        let avgStepTime = Array.apply(null, Array(scenario.steps.length)).map(v => { return { nb: 0, val: 0 }; });
                        let watchTime = Array.apply(null, Array(scenario.steps.length)).map(() => 0);

                        for (let i = 0; i < sessions.length; i++) {
                            for (let j = 0; j < sessions[i].playedSteps.length; j++) {
                                const step = sessions[i].playedSteps[j];
                                let stepIndex = scenario.steps.findIndex(s => s.id == step.step_id);
                                avgStepTime[stepIndex].nb++;
                                avgStepTime[stepIndex].val += step.time;
                                watchTime[stepIndex]++;
                            }
                        }
                        let avgScenarioTime = avgStepTime.map(s => s.val).reduce((a, b) => a + b);

                        for (let j = 0; j < scenario.steps.length; j++) {
                            if (avgStepTime[j].nb != 0)
                                avgStepTime[j].val /= avgStepTime[j].nb;
                            watchTime[j] /= sessions.length;
                        }
                        let labels = scenario.steps.map(s => s.name);

                        let accumulator = 0;
                        addChartToList(charts, "Temps moyen par étape (s)", TYPE.LINE, labels, [
                            { label: "Temps relatif", data: avgStepTime.map(t => t.val) },
                            { label: "Temps absolu", data: avgStepTime.map(t => accumulator += t.val) }
                        ]);
                        accumulator = 0;
                        addChartToList(charts, "Taux de réalisation d'une étape (%)", TYPE.LINE, labels, [
                            { label: "Taux relatif", data: watchTime.map(v => v * 100) },
                            // { label: "Taux absolu", data: watchTime.map(v => { accumulator += v * 100; return accumulator; }) }
                        ]);
                        addInfoBoxToList(infoBoxes, "Temps moyen total", stringTime(avgScenarioTime));
                        addInfoBoxToList(infoBoxes, "Nombre de sessions", sessions.length);
                        addInfoBoxToList(infoBoxes, "Taux moyen de saut d'étape", Math.round(avgStepTime.filter(s => s.nb == 0).length / scenario.steps.length * 100) + "%");
                        hideLoading();
                        resolve();
                    }
                }
            }).catch(err => {
                hideLoading();
                resolve();
            });
        });
    });
}

export default {
    addChartToList,
    addInfoBoxToList,
    generateStatistics,
    generateUserStatistics,
    generateScenarioStatistics,
    generateUserScenarioStatistics
}