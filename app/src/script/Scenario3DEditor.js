import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { TTFLoader } from "three/examples/jsm/loaders/TTFLoader";
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
const loaderTTF = new TTFLoader();
const loaderFont = new FontLoader();


let __font = null;
/**
 * Returns the font used for 3D text rendering (if not loaded, load it first)
 * @returns The font user for text rendering
 */
function getFont() {
    return new Promise((resolve, reject) => {
        if (__font != null) resolve(__font);
        const FONT_URL = window.location.origin + "/fonts/Roboto-Regular.ttf";
        loaderTTF.load(FONT_URL, f => {
            const font = loaderFont.parse(f);
            __font = font;
            resolve(font)
        });
    });
}

/**
 * Checks for canvas setup, three.js setup and starts rendering if not started
 */
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
/**
 * Resize the given canvas to the new 3D view
 * @param {HTMLCanvasElement} canvas canvas used for three.js rendering
 * @param {THREE.Camera} camera Three js camera used for rendering
 * @param {THREE.Renderer} renderer Three js renderer used for rendering
 */
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

/**
 * Adds a new text label to the scene (the position attribute is modified when the user moves the label in the editor)
 * @param {string} text Text to render
 * @param {{x:number,y:number,z:number}} position Position of the text
 */
function setLabel(text, position) {
    clearLabels();
    labels.push(new Label(
        text, position
    ));
}

/**
 * Clears all the labels from the scene
 */
function clearLabels() {
    transformControls.detach();
    labels.forEach(l => scene.remove(l.model));
    labels.splice(0, labels.length);
}

/**
 * Label class, contains the text, the position and the 3D model displayed
 */
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
    /**
     * Label constructor, creates the 3D model and adds it to the scene
     * @param {string} text Text of the label
     * @param {{x:number,y:number,z:number}} position Position of the label
     */
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

    /**
     * Updates the label (follows the camera)
     * @param {number} dt frame delta time
     */
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

/**
 * Setups the three.js scene, renderer, camera, controls, etc.
 * @param {HTMLCanvasElement} canvas canvas used for three.js rendering
 */
function setupThree(canvas) {
    // create the scene, camera and renderer
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera( 75, canvas.width / canvas.height, 0.1, 1000 );
    renderer = new THREE.WebGLRenderer({canvas: canvas, alpha: true});

    // enable shadows for the renderer
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ReinhardToneMapping;
    renderer.toneMappingExposure = 2.5;
    // set the resize callback and resize the canvas
    window.onresize = ev => {resizeCanvas(canvas, camera, renderer);};
    window.onresize();

    // add an ambient light (to avoid black shadows)
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    { // add the first light
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.castShadow = true;
        light.shadow.bias = -0.0001;
        light.shadow.mapSize.width = 1024;
        light.shadow.mapSize.height = 1024;
        light.position.set(1, 2, 2);
        scene.add(light);
    }
    { // add the second light
        const light = new THREE.DirectionalLight(0xffffff, 0.5);
        light.castShadow = true;
        light.shadow.bias = -0.0001;
        light.shadow.mapSize.width = 1024;
        light.shadow.mapSize.height = 1024;
        light.position.set(2, 2, -1);
        scene.add(light);
    }
    // set the scene's floor (gray plane)
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), new THREE.MeshStandardMaterial({color: 0x404040}));
    ground.rotation.set(-Math.PI/2, 0, 0);
    ground.receiveShadow = true;
    scene.add(ground);

    // if the machine is already selected before the scene is loaded, add it to the scene
    if (machineModel != null)
        scene.add(machineModel);
    // if a label is edited, show it
    labels.forEach(l => scene.add(l.model));

    // set the default camera position and set the orbit controls
    camera.position.set(2, 2, 2);
    orbitControls = new OrbitControls( camera, renderer.domElement );
    orbitControls.update();

    // init the transform controls (and attach the edited label to it if needed)
    transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.detach();
    if (labels.length > 0) transformControls.attach(labels[0].model);
    transformControls.addEventListener('mouseDown', function () {
        orbitControls.enabled = false; // to avoid rotating the camera when moving the object
    });
    transformControls.addEventListener('mouseUp', function () {
        orbitControls.enabled = true; // to enable camera rotation when we are done moving the object
    });
    scene.add(transformControls);
}

/**
 * Enables three.js rendering (called when the canvas is displayed)
 */
function startRendering() {
    if (isRendering) return;
    isRendering = true;
    renderer.setAnimationLoop(gameloop);
}

/**
 * Disables three.js rendering (called when the canvas is hidden)
 */
function stopRendering() {
    if (!isRendering) return;
    isRendering = false;
    renderer.setAnimationLoop(null);
}

let lastTime = 0;
/**
 * Main gameloop, updates the labels, the controls, and renders the scene
 * @param {number} time absolute time since three.js initialization (in ms)
 */
const gameloop = (time) => {
    const dt = time/1000 - lastTime/1000;
    lastTime = time;
    camera.lookAt(0, 0.5, 0);

    orbitControls.update();
    labels.forEach(l => l.update(dt));
    renderer.render(scene, camera);
};

/**
 * Sets the machine displayed in the scene (from the machine's ID).
 * Makes an API call to retreive the machine's model, and then displays it
 * @param {number} machineID ID of the machine to show
 */
function set3DMachineModel(machineID) {
    if (machineModel != null)
        scene.remove(machineModel);

    // we could use the API url directly in the loader,
    // but just to be able to see if the status code is correct,
    // we do a fetch in the url and recreate a blob url for the loader after
    fetch(API.API_URL+`/scenarios/machines/${machineID}/model`).then(res => {
        if (res.status == 200) {
            // when the model is received, get the blob object
            res.blob().then(data => {
                // generate a local url to use the blob object
                let url = URL.createObjectURL(data);
                // load the blob object as a GLTF model
                loaderGLTF.loadAsync(url).then(obj => {
                    machineModel = obj.scene;
                    machineModel.traverse(child => {
                        // for each mesh child, enable shadows
                        // and if the material is glass, make it transparent
                        if (child.isMesh) {
                            if (child.material.name.includes("vitre")) {
                                child.material.transparent = true;
                                child.material.opacity = 0.4;
                            }
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    });
                    // add the model to the scene (is the scene exists, else it will be added when the scene is loaded)
                    if (scene != null)
                        scene.add(machineModel);
                }).catch(err => {console.error(err);})
            })
        } else { // error
            console.error(res);
        }
    }).catch(err => {console.error(err);});
}

/**
 * Displays or hides the move controls of the editor
 * @returns {number} if the controls are displayed or not
 */
function toogleTransformEnabled() {
    if (transformControls.object == null && labels.length > 0)
        transformControls.attach(labels[0].model);
    else transformControls.detach();
    return transformControls.object != null;
}

/**
 * Resets the camera's transform to focus the machine at the scene's center
 */
function resetCameraTransform() {
    camera.position.set(2, 2, 2);
    camera.lookAt(0, 0, 0);
    orbitControls.reset();
}

export {
    checkForCanvasSetup,
    stopRendering,
    startRendering,
    set3DMachineModel,
    toogleTransformEnabled,
    setLabel,
    clearLabels,
    resetCameraTransform
};