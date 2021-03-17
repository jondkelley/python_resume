const styles0 = [
  'color: black',
  'background: gray',
  'font-size: 10px',
  'padding: 10px',
].join(';');

const styles1 = [
  'color: black',
  'background: gray',
  'font-size: 15px',
  'padding: 10px',
].join(';');

console.log('%c If you\'re this interested in my code...', styles0);
console.log('%c 😉 You should hire me! 😉', styles1);


function yourFunction() {
      const hide = document.getElementById("hide");
      hide.className =
        hide.className === "hide"
          ? (hide.className = "example removeHide")
          : (hide.className = "hide");
      setTimeout(yourFunction, 1500);
    }
    yourFunction();
