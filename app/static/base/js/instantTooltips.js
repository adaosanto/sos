// textFrom : String, the attribute from which the text
//            should come,
// delta :    String or Number, the distance from the cursor at
//            which the tooltip should appear
function instantTooltips(textFrom, delta) {
  // if delta exists, and can be parsed to a number, we use it,
  // otherwise we use the default of 5:
  delta = parseFloat(delta) ? parseFloat(delta) : 5;

  // function to handle repositioning of the created tooltip:
  function reposition(e) {
    // get the tooltip element:
    var tooltip = this.nextSibling;
    // setting the position according to the position of the
    // pointer:
    tooltip.style.top = (e.pageY + delta) + 'px';
    tooltip.style.left = (e.pageX + delta) + 'px';
  }

  // get all elements that have an attribute from which we
  // want to get the tooltip text from:
  var toTitle = document.querySelectorAll('[' + textFrom + ']'),
    //create a span element:
    span = document.createElement('span'),
    // find if we should use textContent or innerText (IE):
    textProp = 'textContent' in document ? 'textContent' : 'innerText',
    // caching variables for use in the upcoming forEach:
    parent, spanClone;
  // adding a class-name (for CSS styling):
  span.classList.add('createdTooltip');
  // iterating over each of the elements with a title attribute:
  [].forEach.call(toTitle, function(elem) {
    // reference to the element's parentNode:
    parent = elem.parentNode;
    // cloning the span, to avoid creating multiple elements:
    spanClone = span.cloneNode();
    // setting the text of the cloned span to the text
    // of the attribute from which the text should be taken:
    spanClone[textProp] = elem.getAttribute(textFrom);

    // inserting the created/cloned span into the
    // document, after the element:
    parent.insertBefore(spanClone, elem.nextSibling);

    // binding the reposition function to the mousemove
    // event:
    elem.addEventListener('mousemove', reposition);

    // we're setting textFrom attribute to an empty string
    // so that the CSS will still apply, but which
    // shouldl still not be shown by the browser:
    elem.setAttribute(textFrom, '');
  });
}

// calling the function:
instantTooltips('title', 15);