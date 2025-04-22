// Creates an HTML element from an HTML string.
export const createElement = (htmlString) => {
  let wrapper = document.createElement("div");
  wrapper.innerHTML = htmlString.trim();
  return wrapper.firstChild;
};
