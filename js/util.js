// Creates an HTML element from an HTML string.
export function createElement(htmlString) {
  let wrapper = document.createElement("div");
  wrapper.innerHTML = htmlString.trim();
  return wrapper.firstChild;
}
