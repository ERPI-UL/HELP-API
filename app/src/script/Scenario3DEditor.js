import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { TransformControls } from "three/examples/jsm/controls/TransformControls";
import API from "./API";

let isSetup = false;
let isRendering = false;

function checkForCanvasSetup() {
    if (isSetup) return;
    isSetup = true;

    /**@type {HTMLCanvasElement} */
    const canvas = document.getElementById("3D-view");
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width; canvas.height = rect.height;
    setupThree(canvas);
}

let timeoutID = -1;
function resizeCanvas(canvas, camera, renderer) {
    if (timeoutID > 0) clearTimeout(timeoutID);
    
    timeoutID = setTimeout(() => {
        timeoutID = -1;
        const width = canvas.clientWidth; const height = canvas.clientHeight;
        canvas.width = width; canvas.height = height;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setViewport(0, 0, width, height);
    }, 200);
}

let scene = null
let camera = null
let renderer = null
let machineModel = null;
let controls = null;
const pointer = new THREE.Vector2(0.5, 0.5);

function setupThree(canvas) {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera( 75, canvas.width / canvas.height, 0.1, 1000 );
    renderer = new THREE.WebGLRenderer({canvas: canvas, alpha: true});

    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ReinhardToneMapping;
    renderer.toneMappingExposure = 2.5;
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    window.onresize = ev => {resizeCanvas(canvas, camera, renderer);};

    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    {
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.castShadow = true;
        light.shadow.bias = -0.0001;
        light.shadow.mapSize.width = 1024;
        light.shadow.mapSize.height = 1024;
        light.position.set(1, 2, 2);
        scene.add(light);
    }
    {
        const light = new THREE.DirectionalLight(0xffffff, 0.5);
        light.castShadow = true;
        light.shadow.bias = -0.0001;
        light.shadow.mapSize.width = 1024;
        light.shadow.mapSize.height = 1024;
        light.position.set(2, 2, -1);
        scene.add(light);
    }
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), new THREE.MeshStandardMaterial({color: 0xffffff}));
    ground.rotation.set(-Math.PI/2, 0, 0);
    ground.receiveShadow = true;
    scene.add(ground);

    if (machineModel != null)
        scene.add(machineModel);

    controls = new TransformControls(camera, renderer.domElement);
    controls.attach(machineModel??ground);
    scene.add(controls);

    canvas.addEventListener("click", ev => {
        const rect = canvas.getBoundingClientRect();
        pointer.x = (ev.x - rect.left) * 2 / rect.width - 1;
        pointer.y = (ev.y - rect.top) * -2 / rect.height + 1;
        console.log(pointer.x, pointer.y)

        const rayCaster = new THREE.Raycaster();
        rayCaster.setFromCamera(pointer, camera);
        const intersections = rayCaster.intersectObjects(scene.children);
        controls.detach();
        controls.attach(intersections[0].object);
    });
}

function startRendering() {
    if (isRendering) return;
    isRendering = true;
    renderer.setAnimationLoop(gameloop);
}

function stopRendering() {
    if (!isRendering) return;
    isRendering = false;
    renderer.setAnimationLoop(null);
}

let lastTime = 0;
const gameloop = (time) => {
    const dt = time - lastTime;
    lastTime = time;
    camera.lookAt(0, 0.5, 0);

    camera.position.set(Math.cos(time/4000)*2, 2, Math.sin(time/4000)*2);
    renderer.render(scene, camera);
};

function set3DMachineModel(machineID) {
    // we could use the API url directly in the loader,
    // but just to be able to see if the status code is correct,
    // we do a fetch in the url and recreate a blob url for the loader after
    fetch(API.API_URL+`/scenarios/machines/${machineID}/model`).then(res => {
        if (res.status == 200) {
            res.blob().then(data => {
                let url = URL.createObjectURL(data);
                const loader = new GLTFLoader();
                loader.loadAsync(url).then(obj => {
                    machineModel = obj;
                    obj.scene.traverse(child => {
                        if (child.isMesh) {
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    })
                    if (scene != null) {
                        scene.add(obj.scene);
                        controls.attach(obj.scene);
                    }
                }).catch(err => {console.error(err);})
            })
        } else { // error
            console.error(res);
        }
    }).catch(err => {console.error(err);});
}

function setControlMode(mode) {
    controls.setMode(mode);
}

export {
    checkForCanvasSetup,
    stopRendering,
    startRendering,
    set3DMachineModel,
    setControlMode
};