"use strict";

window.addEventListener('DOMContentLoaded', () => {

  // image stuff

  function hideAllImages() {
    images.forEach(item => {
      item.setAttribute("style", "display: none");
    })
  }

  function unpressAllImageButtons() {
    buttons.forEach(item => {
      item.setAttribute("class", "button");
    })
  }

  function initImages() {
    hideAllImages();
    images[0].setAttribute("style", "display: initial");
    images.forEach((item, key) => {
      var newButton = document.createElement("button");
      newButton.setAttribute("class", "button");
      newButton.innerHTML = key + 1;
      if (key == 0) {
        newButton.classList.add("class", "pressed");
      }
      buttonDiv.appendChild(newButton);
    })
  }

  const images = document.querySelectorAll('.image');
  const frame = document.querySelector('.images');
  const buttonDiv = document.querySelector('.buttons');

  try {
    initImages();
  } catch (error) {
    frame.setAttribute("style", "display: none");
  }

  const buttons = document.querySelectorAll('.button');


  buttons.forEach((item, key) => {
    item.innerHTML = key + 1;
    item.addEventListener('click', event => {
      hideAllImages();
      unpressAllImageButtons();
      images[key].setAttribute("style", "display: initial");
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
  const completeButton = document.querySelector('.complete')

  hideAllStages();
  initStageButtons();
});