import { PoseLandmarker, FilesetResolver, DrawingUtils } from "https://cdn.skypack.dev/@mediapipe/tasks-vision@0.10.0";

const POSE_LANDMARKS = {
  NOSE: 0,
  LEFT_EYE_INNER: 1,
  LEFT_EYE: 2,
  LEFT_EYE_OUTER: 3,
  RIGHT_EYE_INNER: 4,
  RIGHT_EYE: 5,
  RIGHT_EYE_OUTER: 6,
  LEFT_EAR: 7,
  RIGHT_EAR: 8,
  MOUTH_LEFT: 9,
  MOUTH_RIGHT: 10,
  LEFT_SHOULDER: 11,
  RIGHT_SHOULDER: 12,
  LEFT_ELBOW: 13,
  RIGHT_ELBOW: 14,
  LEFT_WRIST: 15,
  RIGHT_WRIST: 16,
  LEFT_PINKY: 17,
  RIGHT_PINKY: 18,
  LEFT_INDEX: 19,
  RIGHT_INDEX: 20,
  LEFT_THUMB: 21,
  RIGHT_THUMB: 22,
  LEFT_HIP: 23,
  RIGHT_HIP: 24,
  LEFT_KNEE: 25,
  RIGHT_KNEE: 26,
  LEFT_ANKLE: 27,
  RIGHT_ANKLE: 28,
  LEFT_HEEL: 29,
  RIGHT_HEEL: 30,
  LEFT_FOOT_INDEX: 31,
  RIGHT_FOOT_INDEX: 32
};

const webcamSection = document.getElementById("webcamsection");
let poseLandmarker = undefined;
let runningMode = "IMAGE";
let enableWebcamButton;
let webcamRunning = false;
let video_constraints = true;
const videoHeight = "480px";
const videoWidth = "360px";
// Before we can use PoseLandmarker class we must wait for it to finish
// loading. Machine Learning models can be large and take a moment to
// get everything needed to run.
const createPoseLandmarker = async () => {
  const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm");
  poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath: `https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task`,
      delegate: "GPU"
    },
    runningMode: runningMode,
    numPoses: 1
  });
  webcamSection.classList.remove("invisible");
};
createPoseLandmarker();



let switchCamButton = document.getElementById("switchCamButton");
switchCamButton.addEventListener("click", switchCam);

/********************************************************************
// Demo 2: Continuously grab image from webcam stream and detect it.
********************************************************************/
const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");
const drawingUtils = new DrawingUtils(canvasCtx);
// Check if webcam access is supported.
// const hasGetUserMedia = () => { var _a; return !!((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia); };
// // If webcam supported, add event listener to button for when user
// // wants to activate it.
// if (hasGetUserMedia()) {
//   enableWebcamButton = document.getElementById("webcamButton");
//   enableWebcamButton.addEventListener("click", enableCam);
// }
// else {
//   console.warn("getUserMedia() is not supported by your browser");
// }
// Enable the live webcam view and start detection.
function startCam() {
  if (!poseLandmarker) {
    console.log("Wait! poseLandmaker not loaded yet.");
    return;
  }

  // getUsermedia parameters.
  const constraints = {
    video: video_constraints,
    width: 360,
    height: 480,
  };
  
  // Activate the webcam stream.
  navigator.mediaDevices.getUserMedia(constraints)
  .then((stream) => {
    video.srcObject = stream;
    video.addEventListener("loadeddata", predictWebcam);
  })
  .catch((e) => {
    constraints.video = true;
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
      video.srcObject = stream;
      video.addEventListener("loadeddata", predictWebcam);
    });
  });  
  webcamRunning = true;
}

function stopWebcam() {
  // if (webcamRunning !== enable) {
  if (video.srcObject !== null) {
    video.removeEventListener("loadeddata", predictWebcam);
    if (video.srcObject !== null) {
      const tracks = video.srcObject.getTracks();
      if (tracks.length > 0) {
        tracks[0].stop();  
      }  
    }
  }
  webcamRunning = false;
}

function switchCam() {
  stopWebcam();
  if (video_constraints === true) {
    video_constraints = {
      facingMode: {
        exact: "environment"
      }
    };
  } else {
    video_constraints = {
      facingMode: {
        exact: "user"
      }
    };
  }
  startCam();
}


let lastVideoTime = -1;
let dir = [];
let steering = [];
const BUFFER_SIZE = 3;
const FWD = 1;
const NONE = 0;
const REV = -1;
const LFT = -1;
const RGT = 1;



async function predictWebcam() {
  canvasElement.style.height = videoHeight;
  video.style.height = videoHeight;
  canvasElement.style.width = videoWidth;
  video.style.width = videoWidth;
  // Now let's start detecting the stream.
  if (runningMode === "IMAGE") {
    runningMode = "VIDEO";
    await poseLandmarker.setOptions({ runningMode: "VIDEO" });
  }
  let startTimeMs = performance.now();
  if (lastVideoTime !== video.currentTime) {
    lastVideoTime = video.currentTime;
    poseLandmarker.detectForVideo(video, startTimeMs, (result) => {
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      for (const landmark of result.landmarks) {
        drawingUtils.drawLandmarks(landmark, {
          radius: (data) => DrawingUtils.lerp(data.from.z, -0.15, 0.1, 5, 1)
        });
        drawingUtils.drawConnectors(landmark, PoseLandmarker.POSE_CONNECTIONS);
      }
      canvasCtx.restore();

      let cur_dir = NONE;
      if (result.worldLandmarks.length > 0) {
        // mediapipe coordinate system:
        // * x towards left hip
        // * y towards ground
        // * z towards back
        let nose = result.worldLandmarks[0][POSE_LANDMARKS.NOSE];
        let rw = result.worldLandmarks[0][POSE_LANDMARKS.RIGHT_WRIST];
        let lw = result.worldLandmarks[0][POSE_LANDMARKS.LEFT_WRIST];
        
        if (rw.y < nose.y) {
          // Right hand is up
          cur_dir = FWD;
          
          let v_rw = [rw.x, rw.y, rw.z];
          let re = result.worldLandmarks[0][POSE_LANDMARKS.RIGHT_ELBOW];
          let v_re = [re.x, re.y, re.z];
          let v_wrist_elbow = subtactVector(v_rw, v_re);
          v_wrist_elbow = mulVector(v_wrist_elbow, -1)
          // let rs = result.worldLandmarks[0][POSE_LANDMARKS.RIGHT_SHOULDER];          

          // let angleMove = Math.atan2(v_wrist_elbow[2], v_wrist_elbow[1]) * 180 / Math.PI;
          let angleDir = Math.atan2(v_wrist_elbow[0], v_wrist_elbow[2]) * 180 / Math.PI;
    
          if (angleDir > 40) {
              appendCmd(cur_dir, RGT);
          } else if (angleDir < -40) {
              appendCmd(cur_dir, LFT);
          } else {
            appendCmd(cur_dir, NONE);
          }
        } else if (lw.y < nose.y) {
          // Left hand is up
          cur_dir = REV;

          let v_lw = [lw.x, lw.y, lw.z];
          let le = result.worldLandmarks[0][POSE_LANDMARKS.LEFT_ELBOW];
          let v_le = [le.x, le.y, le.z];
          let v_wrist_elbow = subtactVector(v_lw, v_le);
          v_wrist_elbow = mulVector(v_wrist_elbow, -1)
          // let ls = result.worldLandmarks[0][POSE_LANDMARKS.LEFT_SHOULDER];          

          // let angleMove = Math.atan2(v_wrist_elbow[2], v_wrist_elbow[1]) * 180 / Math.PI;
          let angleDir = Math.atan2(v_wrist_elbow[0], v_wrist_elbow[2]) * 180 / Math.PI;
    
          if (angleDir > 40) {
              appendCmd(cur_dir, RGT);
          } else if (angleDir < -40) {
              appendCmd(cur_dir, LFT);
          } else {
            appendCmd(cur_dir, NONE);
          }
        } 

        if (cur_dir === NONE) {
          cur_cmd = "";
        } else {
          let cmd_dir = "";
          let cmd_steer = "";
          let sum_dir = dir.reduce((partialSum, a) => partialSum + a, 0)
          if (sum_dir > 0) {
            cmd_dir = "fwd";
          } else if (sum_dir < 0) {
            cmd_dir = "rev";
          }
          let sum_steer = steering.reduce((partialSum, a) => partialSum + a, 0)
          if (sum_steer > 0) {
            cmd_steer = "rgt";
          } else if (sum_steer < 0) {
            cmd_steer = "lft";
          }

          if (cmd_dir.length > 0) {
            cur_cmd = cmd_dir;
            if (cmd_steer.length > 0) {
              cur_cmd += "|" + cmd_steer;
            }
          }



          // console.log(cur_cmd, "XYZ", v_rw);
          console.log(cur_cmd)

          // }
          // console.log("Move:", angleMove, "DIR: ", angleDir);
          // console.log("Y:", rw.y);
        }
      }
    });
  }
  // Call this function again to keep predicting when the browser is ready.
  if (webcamRunning === true) {
    window.requestAnimationFrame(predictWebcam);
  }
}

function appendCmd(cur_dir, cur_steer) {
  if (dir.length == BUFFER_SIZE) {
    dir.shift();
    steering.shift();
  }
  dir.push(cur_dir);
  steering.push(cur_steer);
}


function angleBetween(p1, p2) {
  // angle in radians
  // var angleRadians = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]);

  // angle in degrees
  var angleDeg = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / Math.PI;

  return angleDeg
}

function cosinesim(A, B) {
  var dotproduct = 0;
  var mA = 0;
  var mB = 0;

  for (var i = 0; i < A.length; i++) {
    dotproduct += A[i] * B[i];
    mA += A[i] * A[i];
    mB += B[i] * B[i];
  }

  mA = Math.sqrt(mA);
  mB = Math.sqrt(mB);
  var similarity = dotproduct / (mA * mB);

  return similarity;
}

function addVector(a, b) {
  return a.map((e, i) => e + b[i]);
}

function mulVector(a, b) {
  return a.map((e, i) => e * b);
}
function subtactVector(a, b) {
  return a.map((e, i) => e - b[i]);
}

