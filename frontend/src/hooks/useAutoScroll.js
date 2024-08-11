import { useEffect, useLayoutEffect,  useRef } from 'react';

function useAutoScroll(active) {
  const scrollContentRef = useRef(null);
  const isDisabled = useRef(false);
  const prevScrollTop = useRef(null);

  useEffect(() => {
    const resizeObserver = new ResizeObserver(() => {
      if (
        !isDisabled.current &&
        document.documentElement.scrollHeight - window.innerHeight > window.scrollY
      ) {
        window.scrollTo({
          top: document.documentElement.scrollHeight,
          behavior: 'smooth'
        });
      }
    });

    if (scrollContentRef.current) {
      resizeObserver.observe(scrollContentRef.current);
    }
    
    return () => resizeObserver.disconnect();
  }, []);

  useEffect(() => {
    function onScroll() {
      if (!isDisabled.current && window.scrollY < prevScrollTop.current) {
        isDisabled.current = true;
      } else if (
        isDisabled.current &&
        document.documentElement.scrollHeight - window.innerHeight === window.scrollY
      ) {
        isDisabled.current = false;
      }
      prevScrollTop.current = window.scrollY;
    }
    
    window.addEventListener('scroll', onScroll);

    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useLayoutEffect(() => {
    isDisabled.current = false;
    prevScrollTop.current = window.scrollY;
  }, [active]);


  return scrollContentRef;
}

export default useAutoScroll;