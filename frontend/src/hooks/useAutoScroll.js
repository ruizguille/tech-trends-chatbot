import { useEffect, useLayoutEffect,  useRef } from 'react';

function useAutoScroll(active) {
  const scrollRef = useRef(null);
  const scrollContentRef = useRef(null);
  const isDisabled = useRef(false);
  const prevScrollTop = useRef(null);

  useEffect(() => {
    const resizeObserver = new ResizeObserver(() => {
      if (
        !isDisabled.current &&
        scrollRef.current.scrollHeight - scrollRef.current.clientHeight > scrollRef.current.scrollTop
      ) {
        scrollRef.current.scrollTo({
          top: scrollRef.current.scrollHeight,
          behavior: 'smooth'
        });
      }
    });
    resizeObserver.observe(scrollContentRef.current);
    
    return () => resizeObserver.disconnect();
  }, []);

  useEffect(() => {
    function onScroll() {
      if (!isDisabled.current && scrollRef.current.scrollTop < prevScrollTop.current) {
        isDisabled.current = true;
      } else if (
        isDisabled.current &&
        scrollRef.current.scrollHeight - scrollRef.current.clientHeight === scrollRef.current.scrollTop
      ) {
        isDisabled.current = false;
      }
      prevScrollTop.current = scrollRef.current.scrollTop;
    }
    
    scrollRef.current.addEventListener('scroll', onScroll);
    const scrollRefValue = scrollRef.current;

    return () => scrollRefValue.removeEventListener('scroll', onScroll);
  }, []);

  useLayoutEffect(() => {
    isDisabled.current = false;
    prevScrollTop.current = scrollRef.current.scrollTop;
  }, [active]);


  return { scrollRef, scrollContentRef };
}

export default useAutoScroll;