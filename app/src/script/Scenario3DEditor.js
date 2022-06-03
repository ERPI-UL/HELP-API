import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { FontLoader } from "three/examples/jsm/loaders/FontLoader";
import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { TransformControls } from "three/examples/jsm/controls/TransformControls";
import API from "./API";

/**@type {Label[]} */
let labels = [];
/**@type {THREE.Scene} */
let scene = null
/**@type {THREE.Camera} */
let camera = null
/**@type {THREE.Renderer} */
let renderer = null
/**@type {THREE.Mesh} */
let machineModel = null;
/**@type {OrbitControls} */
let orbitControls = null;
/**@type {transformControls} */
let transformControls = null;
// const pointer = new THREE.Vector2(0.5, 0.5);
let isSetup = false;
let isRendering = false;
const loaderGLTF = new GLTFLoader();
const loaderFont = new FontLoader();


let __font = null;
function getFont() {
    return new Promise((resolve, reject) => {
        if (__font != null) resolve(__font);
        const FONT_URL = "https://raw.githubusercontent.com/FurWaz/furwaz.github.io/main/resources/fonts/Roboto_Regular.json";
        loaderFont.load(FONT_URL, f => {
            __font = f;
            resolve(__font);
        });
    });
}

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

function setLabel(text, position) {
    clearLabels();
    labels.push(new Label(
        text, position
    ));
}

function clearLabels() {
    transformControls.detach();
    labels.forEach(l => scene.remove(l.model));
    labels.splice(0, labels.length);
}

class Label {
    static LABEL_ID_COUNTER = 1;
    id = Label.LABEL_ID_COUNTER++;
    text = "";
    position = {x: 0, y: 0, z: 0}
    /**@type {THREE.Group} */
    model = null
    /**@type {THREE.Mesh} */
    txtMesh = null;
    lookAtPos = new THREE.Vector3();
    constructor(text, position) {
        this.text = text;
        this.position = position;
        this.model = new THREE.Group();
        this.model.receiveShadow = true;
        this.model.castShadow = true;
        this.model.position.set(position.x, position.y, position.z);
        getFont().then(font => {
            // text mesh
            this.txtMesh = new THREE.Mesh(
                new TextGeometry(this.text, {
                    font: font,
                    size: 0.03,
                    height: 0.002
                }),
                new THREE.MeshToonMaterial({color: 0xffffff})
            );
            this.txtMesh.receiveShadow = true;
            this.txtMesh.castShadow = true;
            this.txtMesh.geometry.center();
            this.model.add(this.txtMesh);

            // back mesh
            const dims = text.trim().length > 0 ? this.txtMesh.geometry.boundingBox : {min: {x: 0, y: 0}, max: {x: 0, y: 0}};
            this.model.add(new THREE.Mesh(
                new THREE.PlaneBufferGeometry(dims.max.x - dims.min.x + 0.02, dims.max.y - dims.min.y + 0.02),
                new THREE.MeshLambertMaterial({color: 0x101010}))
            );
        })
        if (scene) scene.add(this.model);
        if (transformControls) {
            if (transformControls.object == null)
                transformControls.detach();
            transformControls.attach(this.model);
        }
    }

    update(dt) {
        if (this.txtMesh) {
            this.lookAtPos.add(
                new THREE.Vector3(
                    camera.position.x,
                    camera.position.y,
                    camera.position.z
                ).sub(this.lookAtPos)
                .multiply(new THREE.Vector3(dt*2, dt*2, dt*2))
            );
            this.model.lookAt(this.lookAtPos);
            const pos = this.model.position;
            this.position.x = pos.x;
            this.position.y = pos.y;
            this.position.z = pos.z;
        }
    }
}

function setupThree(canvas) {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera( 75, canvas.width / canvas.height, 0.1, 1000 );
    renderer = new THREE.WebGLRenderer({canvas: canvas, alpha: true});

    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ReinhardToneMapping;
    renderer.toneMappingExposure = 2.5;
    window.onresize = ev => {resizeCanvas(canvas, camera, renderer);};
    window.onresize();

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
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), new THREE.MeshStandardMaterial({color: 0x404040}));
    ground.rotation.set(-Math.PI/2, 0, 0);
    ground.receiveShadow = true;
    scene.add(ground);

    if (machineModel != null)
        scene.add(machineModel);
    labels.forEach(l => scene.add(l.model));

    camera.position.set(2, 2, 2);
    orbitControls = new OrbitControls( camera, renderer.domElement );
    orbitControls.update();

    transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.detach();
    if (labels.length > 0) transformControls.attach(labels[0].model);
    transformControls.addEventListener('mouseDown', function () {
        orbitControls.enabled = false;
    });
    transformControls.addEventListener('mouseUp', function () {
        orbitControls.enabled = true;
    });
    scene.add(transformControls);
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
    const dt = time/1000 - lastTime/1000;
    lastTime = time;
    camera.lookAt(0, 0.5, 0);

    orbitControls.update();
    labels.forEach(l => l.update(dt));
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
                loaderGLTF.loadAsync(url).then(obj => {
                    machineModel = obj.scene;
                    machineModel.traverse(child => {
                        if (child.isMesh) {
                            if (child.material.name.includes("vitre")) {
                                child.material.transparent = true;
                                child.material.opacity = 0.4;
                            }
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    });
                    if (scene != null)
                        scene.add(machineModel);
                }).catch(err => {console.error(err);})
            })
        } else { // error
            console.error(res);
        }
    }).catch(err => {console.error(err);});
}

function toogleTransformEnabled() {
    if (transformControls.object == null && labels.length > 0)
        transformControls.attach(labels[0].model);
    else transformControls.detach();
    return transformControls.object != null;
}

export {
    checkForCanvasSetup,
    stopRendering,
    startRendering,
    set3DMachineModel,
    toogleTransformEnabled,
    setLabel,
    clearLabels
};