import { useState, useLayoutEffect, useRef } from 'react';

function useAutosize(value) {
  const ref = useRef(null);
  const [borderWidth, setBorderWidth] = useState(0);

  useLayoutEffect(() => {
    const style = window.getComputedStyle(ref.current);
    setBorderWidth(parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth));
  }, []);

  useLayoutEffect(() => {
    ref.current.style.height = 'inherit';
    ref.current.style.height = `${ref.current.scrollHeight + borderWidth}px`;
  }, [value, borderWidth]);

  return ref;
}

export default useAutosize;