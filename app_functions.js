// Adds an event listener so that a function is run when the icon is clicked
document.getElementById('dropdown').addEventListener("click", function(){
  // Gets the .links element to be used later in the function
  var links = document.querySelector('.links');
  // This is used in order to get the CSS value of display for .links
  var displayVal = window.getComputedStyle(links).getPropertyValue("display");
  // The if statement checks whether the .links element is displayed
  if (displayVal == "none") {
    // This changes the css of the links so that they are shown
    links.style.cssText = "display: block; background-color: white; \
     box-shadow: 0 4px 7px 1px rgba(0, 0, 0, 0.15); min-width: 10%; \
     text-align: center;";
    // This changes the color of the dropdown icon to yellow
    document.querySelector('header i').style.cssText = "color: yellow;";
  }
  else {
    // This section hides the links once the dropdown icon is clicked again
    links.style.cssText = "display: none;";
    // The dropdown icon is reset to white
    document.querySelector('header i').style.cssText = "color: white;";
  }
});

var idInt = 0;

function test(){
  var value = document.getElementById("portfolioFilter").value;
  if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp = new XMLHttpRequest();
  } else {
      // code for IE6, IE5
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          document.getElementById("portfolio").innerHTML = this.responseText;
      }
  };
    xmlhttp.open("GET","/load/"+value,false);
    xmlhttp.send();


}

function blocFilter() {
  test();
  getIDs();
  document.getElementById('AddBloc').addEventListener("click", function() {
      addBlocModal.style.display = "block";
  });
};

// Code for iterating through child elements derived from:
// http://bit.ly/2gytmY3
function getIDs() {
  [].forEach.call(document.getElementsByClassName('blocs'), function(element) {
    if(element.nextElementSibling != null) {
      element.setAttribute("id", "bloc" + idInt);
      idInt++;
    }
    else if(element.nextElementSibling == null) {
      element.setAttribute("id", "AddBloc");
    }
  });
};

var iCount = 0;
// The drag and drop code has been derived from:
// https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API
function drag(e) {
  var id = e.dataTransfer.setData('text/html', e.target.id);
  e.effectAllowed = 'move';
};

function setDrop(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
};

function drop(e, el) {
  e.preventDefault();
  var id = e.dataTransfer.getData('text/html');
  if (iCount == 0) {
    e.target.innerHTML = "";
  };
  el.insertBefore(document.getElementById(id), el.childNodes[0]);
  if (el == document.getElementById('sentBlocs')) {
    document.getElementById(id).querySelector('input').checked = true;
  }
  else {
    document.getElementById(id).querySelector('input').checked = false;
  }
  el.style.cssText = "text-align: left; border: none; \
   line-height: normal; color: black;";
  iCount++;
};

function checkHasChild() {
  var sendDiv = document.getElementById('sentBlocs');
  var hasChild = sendDiv.hasChildNodes();

  if(hasChild == false) {
    sendDiv.style.border = "1px dashed slategray";
  }
};

function endDrag(e) {
  e.dataTransfer.clearData();
  checkHasChild();
};

function selectAppend(e, el) {
  var sendDiv = document.getElementById('sentBlocs');
  var portfolioDiv = document.getElementById('portfolio');
  // To get the checkbox value check I looked at:
  // http://www.w3schools.com/jsref/prop_checkbox_checked.asp
  if(el.checked == true) {
    if (iCount == 0) {
      sendDiv.innerHTML = "";
    };
    sendDiv.insertBefore(el.parentElement, sendDiv.childNodes[0]);
    sendDiv.style.cssText = "text-align: left; border: none; \
     line-height: normal; color: black;";
    checkHasChild();
    iCount++;
  }
  else {
    portfolioDiv.insertBefore(el.parentElement, portfolioDiv.childNodes[0]);
    checkHasChild();
  }
};

function filterValue() {
    var x = document.getElementById("portfolioFilter").value;
    document.getElementById("demo").innerHTML = "You selected: " + x;
}
function removeEmail(elementID){
document.getElementById("test1").innerHTML = elementID
}

getIDs();
