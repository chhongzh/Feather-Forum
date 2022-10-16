const debounce = (fn, time) => {
  let timeout = null;
  return function () {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => {
      fn.call(this);
    }, time);
  };
};

export default { debounce };
