let speedX = 5;
let speedY = 5;
var sampleSize = 50;
var rectTest;
var agents = [];
var holes = [];
var columnCount;
var rowCount;

var pixelNums = [];
var gender = [];
var heights = [];
var weights = [];
var ap_hi = [];
var ap_lo = [];
var chol = [];
var gluc = [];
var smoke = [];
var alco = [];
var active = [];
var disease = [];

let video;
const devices = [];

function preload(){
  cardio = loadTable('cardio_outliers.csv', 'csv', 'header');
  navigator.mediaDevices.enumerateDevices().then(gotDevices);
}
function setup() {
  pixelDensity(1);
  createCanvas(windowWidth, windowHeight);
  columnCount = cardio.getColumnCount();
  rowCount = cardio.getRowCount();
  //console.log(columnCount, rowCount);
  pixelNums = cardio.getColumn('pixel_number');
  gender = cardio.getColumn('gender');
  heights = cardio.getColumn('height');
  weights = cardio.getColumn('weight');
  ap_hi = cardio.getColumn('ap_hi');
  ap_lo = cardio.getColumn('ap_lo');
  chol = int(cardio.getColumn('cholesterol'));
  gluc = int(cardio.getColumn('gluc'));
  smoke = cardio.getColumn('smoke');
  alco = cardio.getColumn('alco');
  active = cardio.getColumn('active');
  disease = cardio.getColumn('cardio');
  
  //have to make in setup so it doesn't reset to its original position every frame
  
  pixelNums = shuffle(pixelNums);
  //PICK 50 THAT WORK WITHIN 0 AND THE WINDOWWIDTH THAT WILL WORK CAN DO IN GET POS? NEED TO CHANGE WORKFLOW. BIG CHANGE BIG CHANGE. THEY WILL ONLY BE ON THE LEFT SIDE OTHERWISE BIG PROBLEM.
  for(var i = 0; i<sampleSize; i++){ //can't do this for all 1401 outliers, instead need to choose a sample size. going to try 50 to start
    var index = floor(random(0, rowCount));
    var pos = getPos(pixelNums[index]);
    var xPos = pos[0] + floor(random(-weights[index], weights[index]));
    if(xPos<0 || xPos>width){
      xPos = pos[0];
    }
    var yPos = pos[1] + floor(random(-weights[index], weights[index]));
    if(yPos<0||yPos>height){
      yPos = pos[1];
    }
    var size = floor(heights[index]/5);
    holes[i] = makeHole(xPos, yPos, size, size, index);
    agents[i] = makeAgent(holes[i]);
  }

  
}

function gotDevices(deviceInfos){
  for (let i = 0; i !== deviceInfos.length; ++i) {
    const deviceInfo = deviceInfos[i];
    if (deviceInfo.kind == 'videoinput') {
      devices.push({
        label: deviceInfo.label,
        id: deviceInfo.deviceId
      });
    }
  }
  console.log(devices);
  let supportedConstraints = navigator.mediaDevices.getSupportedConstraints();
  console.log(supportedConstraints);
  var constraints = {
    video: {
      deviceId: {
        exact: devices[1].id
      },
    }
  };
  video = createCapture(constraints);
  video.size(windowWidth, windowHeight);
  video.hide();
}

function draw() {
  background(220);
  image(video, 0, 0, windowWidth, windowHeight);
  
  //i want to manage to get a square of pixels to leave a black spot behind, and then those copied pixels to travel with a square across the screen. hopefully demoing the behavior of my larger sketch where the square that is floating (and potentially its behavior) will be informed by a dataset
  //loadPixels();
  noStroke();
  fill("black");
  for(var i = 0; i<holes.length; i++){ //draw the black rectangles
    rect(holes[i].x, holes[i].y, holes[i].w, holes[i].h);
  }
  
  
  for(var j = 0; j<agents.length; j++){ //have to move them first
    agents[j].move();
  }
  video.loadPixels();
  loadPixels(); //load the pixels from the video
  for(var k = 0; k<agents.length; k++){
    agents[k].draw(); //draw each agent (which involves taking the pixels from the video feed and copying them to the moving rectangle)
  }
  updatePixels(); //update after all of these changes have been made
  
  
}

function getPos(pixNum){
  xPos = floor(pixNum/100);
  yPos = pixNum%100*10;
  return [xPos, yPos];
}

function makeHole(x, y, w, h, index){
  let hole = {
    x: floor(x), //these must be integers for this to work!!!!
    y: floor(y),
    w: floor(w),
    h: floor(h),
    index: index
  };
  return hole;
}

function makeAgent(hole){
  let agent = {
    hole: hole,
    x: hole.x,
    y: hole.y,
    index: hole.index,
    vx: random(-(gluc[hole.index]+chol[hole.index]), gluc[hole.index]+chol[hole.index]),
    vy: random(-(gluc[hole.index]+chol[hole.index]), gluc[hole.index]+chol[hole.index]),
    
    move(){ //this is just going to move where the left corner of the hole is that is moving. basic movement right now, the important function is the draw
      
      //NEED TO ADD MOVEMENT SWITCH CASE. CAN DO BASED ON IF THEY'RE ACTIVE OR NOT
      this.x += this.vx;
      this.y += this.vy;
      
      if(this.x<0 || this.x>width){
        this.vx = -this.vx;
      }
      if (this.y < 0 || this.y>height) {
        this.vy = -this.vy;
      } 
    },
    
    draw(){ 
      //get latest video pixels
      video.loadPixels(); //this gets the ones behind the square too;
      
      //for each pixel in the hole region which will have same dimensions as our moving rectangle
      for(var i = 0; i<hole.w; i++){
        for(var j = 0; j<hole.h; j++){
            //where the hole is
            let holeX = hole.x + i;
            let holeY = hole.y + j;
            //where the corresponding moving rectangle pixel is
            let dstX = floor(this.x+i);
            let dstY = floor(this.y+j);
          
            //bounds check. if these are true then we skip the following part of the loop so we don't go out of bounds. these checks are basically just saying we only draw and sample the pixels that are on the screen
          if(holeX<0 || holeX >= width || holeY<0 || holeY>=height || dstX<0 || dstX>=width || dstY<0 || dstY>=height) continue;
            let holeIndex = (holeX + width * holeY) *4;
            let dstIndex = (dstX + width*dstY)*4;
            let r = video.pixels[holeIndex + 0];
            let g = video.pixels[holeIndex + 1];
            let b = video.pixels[holeIndex + 2];
            switch (gender[hole.index]){
              case '1':
                r = lerp(r, 0, 0.1);
                g = lerp(g, 255, 0.1);
                b = lerp(b, 0, 0.1);
                break;
              case '2':
                 r = lerp(r, 255, 0.1);
                 g = lerp(g, 0, 0.1);
                 b = lerp(b, 255, 0.1);
                 break;
            }
            pixels[dstIndex + 0] = r;
            pixels[dstIndex + 1] = g;
            pixels[dstIndex + 2] = b;
            pixels[dstIndex + 3] = 225;

        }
      }
    }
  };
  return agent;
}