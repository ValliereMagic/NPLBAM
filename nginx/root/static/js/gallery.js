"use strict";

window.addEventListener('DOMContentLoaded', () => {

  // make files in to proper types (images or download link)

  // relevant selectors for this section
  const files = document.querySelectorAll('.file');
  const frame = document.querySelector('.images');
  // Iterate through all the files associated with this animal
  files.forEach(item => {
    // value: download link
    // div: external div that will be controlled by the buttons
    // images only
    // img: image element that goes inside div
    // files only
    // header: h2 element that goes inside div
    // button: goes inside div, gets styled as a button
    // a: link that goes inside the button
    var value = item.getAttribute("value");
    var div = document.createElement('div');
    // If the file is an image (the id stores the file type)
    if (item.classList.contains("type_image")) {
      // create image tag, set src and add it to the div
      var img = document.createElement('img');
      img.setAttribute("src", value);
      img.setAttribute("width", "800");
      div.appendChild(img);
    }
    // if it's not an image
    else{
      // make header, get file name without all the extra stuff, add to header
      var header = document.createElement('h2');
      var split_value = value.split("/");
      var second_split_value = split_value[split_value.length - 1].split(/_\d_/, 2)
      header.innerHTML = second_split_value[second_split_value.length - 1];
      header.setAttribute("style", "text-align: center");
      div.appendChild(header);
      // make download button, add to div
      var button = document.createElement('div');
      button.setAttribute("class", "button");
      var a = document.createElement('a');
      a.setAttribute("href", value);
      a.innerHTML = "Download";
      button.appendChild(a);
      div.appendChild(button);
    }
    // add div to the frame
    div.classList.add("image");
    frame.appendChild(div);

  })
  // image stuff

  function hideAllImages() {
    images.forEach(item => {
      item.setAttribute("style", "display: none");
    })
  }

  function unpressAllImageButtons() {
    buttons.forEach(item => {
      item.setAttribute("class", "file_button");
    })
  }

  function initImages() {
    hideAllImages();
    images[0].setAttribute("style", "display: flex");
    images.forEach((item, key) => {
      var newButton = document.createElement("button");
      newButton.setAttribute("class", "file_button");
      newButton.innerHTML = key + 1;
      if (key == 0) {
        newButton.classList.add("class", "pressed");
      }
      buttonDiv.appendChild(newButton);
    })
  }

  const images = document.querySelectorAll('.image');
  const buttonDiv = document.querySelector('.top>.buttons');

  try {
    initImages();
  } catch (error) {
    frame.setAttribute("style", "display: none");
  }

  const buttons = document.querySelectorAll('.top>.buttons>.file_button');


  buttons.forEach((item, key) => {
    item.innerHTML = key + 1;
    item.addEventListener('click', event => {
      hideAllImages();
      unpressAllImageButtons();
      images[key].setAttribute("style", "display: flex");
      item.classList.add("pressed");
    })
  })

  // stage stuff
  function hideAllStages() {
    stages.forEach(item => {
      item.setAttribute("style", "display: none");
    })
  }

  function unpressAllStageButtons() {
    stageButtons.forEach(item => {
      item.setAttribute("class", "button")
    })
  }

  function initStageButtons() {
    stages.forEach((item, key) => {
      stageButtons[key].addEventListener('click', event => { // When the button is pressed...
        hideAllStages();
        unpressAllStageButtons();
        stages[key].setAttribute("style", "display: flex"); // show corresponding stage
        stageButtons[key].classList.add("pressed"); // style button as pressed
        // Hide "Complete Stage" button when...
        if (currentStage.value == 8) { // animal on stage 8
          completeButton.setAttribute("style", "display:none")
        } else if (key == currentStage.value - 1) { // it's the original stage (not 8 though)
          completeButton.setAttribute("style", "display:initial")
        } else { // not the original stage
          completeButton.setAttribute("style", "display:none")
        }
      })
    })
    // set starting button as pressed
    stageButtons[currentStage.value - 1].classList.add("pressed");
    // un-hide current stage
    stages[currentStage.value - 1].setAttribute("style", "display: flex");
    // if it's on stage 8, hide complete stage button
    if (currentStage.value == 8) {
      completeButton.setAttribute("style", "display: none");
    }
  }

  const stageButtons = document.querySelectorAll('.stageButtons>button');
  const stages = document.querySelectorAll('.stage');
  const currentStage = document.querySelector('#current_stage');
  const completeButton = document.querySelector('#complete')

  hideAllStages();
  initStageButtons();
});