"use strict";

window.addEventListener('DOMContentLoaded', () => {

  // The python file creates a hidden input for each file associated with an
  // animal and the javascript turns them into images or download buttons and
  // creates a button to view each image/file while keeping the rest hidden

  // This section makes files into proper their types (images or download link)

  // Relevant selectors for this section
  // Hidden inputs which contain filenames
  const files = document.querySelectorAll('.file');
  //Frame contains all the images
  const frame = document.querySelector('.images');

  // Iterate through all the files associated with this animal and if it is
  // an image, create an image tag for it, if it is not, create a download
  // button for the file
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
    else {
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

  // This section controls the viewing of images/files via buttons

  // Sets all the images/files to hidden
  function hideAllImages() {
    images.forEach(item => {
      item.setAttribute("style", "display: none");
    })
  }

  // Sets all the buttons to their unpressed version
  function unpressAllImageButtons() {
    buttons.forEach(item => {
      item.setAttribute("class", "file_button");
    })
  }

  // Is run when the page loads
  // Hides all images, shows the first one, makes a button for each image,
  // sets the first button to pressed
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

  // Selectors
  // all images/files
  const images = document.querySelectorAll('.image');
  // the div that holds the buttons
  const buttonDiv = document.querySelector('.top>.buttons');
  // Top section of the gallery page
  const topDiv = document.querySelector('.top');

  // If there are no images, hide the whole section
  try {
    initImages();
  } catch (error) {
    topDiv.setAttribute("style", "display: none");
  }

  // All buttons in the button div
  const buttons = document.querySelectorAll('.top>.buttons>.file_button');

  // Add an event listener to each button
  // If it is clicked, it shows the image/file associated with it
  // and hides the others while keeping button styles correct
  buttons.forEach((item, key) => {
    item.innerHTML = key + 1;
    item.addEventListener('click', event => {
      hideAllImages();
      unpressAllImageButtons();
      images[key].setAttribute("style", "display: flex");
      item.classList.add("pressed");
    })
  })

  // This section controls the viewing of the stages

  // Adds event listeners to all 8 buttons which show their respective stages
  // while hiding the others
  // Also controls the complete stage button by only showing it when it's
  // meant to be shown

  // Hides all the stages
  function hideAllStages() {
    stages.forEach(item => {
      item.setAttribute("style", "display: none");
    })
  }

  // Sets all the buttons to an unpressed style
  function unpressAllStageButtons() {
    stageButtons.forEach(item => {
      item.setAttribute("class", "button")
    })
  }

  // Adds event listeners to the buttons 
  function initStageButtons() {
    console.log(currentStage.value)
    stages.forEach((item, key) => {
      stageButtons[key].addEventListener('click', event => { // When the button is pressed...
        hideAllStages();
        unpressAllStageButtons();
        stages[key].setAttribute("style", "display: flex"); // show corresponding stage
        stageButtons[key].classList.add("pressed"); // style button as pressed
        // Hide "Complete Stage" button when...
        if (currentStage.value == 8) { // animal on stage 8
          completeButton[key].setAttribute("style", "display:none")
        } else if (key == currentStage.value - 1) { // it's the original stage (not 8 though)
          completeButton[key].setAttribute("style", "display:initial")
        } else { // not the original stage
          completeButton[key].setAttribute("style", "display:none")
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

  // Relevant selectors
  // Buttons from 1-8 that represent each stage
  const stageButtons = document.querySelectorAll('.stageButtons>button');
  // Each stage form
  const stages = document.querySelectorAll('.stage');
  // Hidden input that had the animals current stage
  const currentStage = document.querySelector('#current_stage');
  // Button to complete the stage
  const completeButton = document.querySelectorAll('.complete')

  hideAllStages();
  initStageButtons();
});