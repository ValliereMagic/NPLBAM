"use strict";

window.addEventListener('DOMContentLoaded', () => {

  function hideAll() {
    images.forEach(item => {
      item.setAttribute("style", "display: none");
    })
  }

  function unpressAll() {
    buttons.forEach(item => {
      item.setAttribute("class", "button")
    })
  }

  function init() {
    hideAll();
    images[0].setAttribute("style", "display: initial");
    images.forEach((item, key) => {
      var newButton = document.createElement("button")
      newButton.setAttribute("class", "button")
      newButton.innerHTML = key + 1;
      if (key == 0){
        newButton.classList.add("class", "pressed")
      }
      buttonDiv.appendChild(newButton)
    })
  }

  const images = document.querySelectorAll('.image');
  const buttonDiv = document.querySelector('.buttons');
  init();
  const buttons = document.querySelectorAll('.button');


  buttons.forEach((item, key) => {
    item.innerHTML = key+1;
    item.addEventListener('click', event => {
      hideAll();
      unpressAll();
      images[key].setAttribute("style", "display: initial");
      item.classList.add("pressed")
    })
  })


});