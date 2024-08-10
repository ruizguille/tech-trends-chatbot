import Markdown from 'react-markdown';
import useAutoScroll from '@/hooks/useAutoScroll';
import Spinner from '@/components/Spinner';
import assistantIcon from '@/assets/images/assistant.svg';
import userIcon from '@/assets/images/user.svg';

function ChatMessages({ messages, isLoading }) {
  const { scrollRef, scrollContentRef } = useAutoScroll(isLoading);
  
  return (
    <div ref={scrollRef} className='grow pt-6 pb-4 px-6 overflow-auto'>
      <div ref={scrollContentRef} className='max-w-[800px] mx-auto space-y-7'>
        {messages.map(({ role, content, loading, error }, idx) => (
          <div key={idx} className='flex items-start gap-4'>
            <img
              className='h-5 w-5 shrink-0 mt-0.5'
              src={role === 'user' ? userIcon : assistantIcon}
              alt='user'
            />
            <div>
              <div className='markdown-container'>
                {(loading && !content) ? <Spinner />
                  : (role === 'assistant')
                    ? <Markdown>{content}</Markdown>
                    : <div className='whitespace-pre-line'>{content}</div>
                }
              </div>
              {error && (
                <div className={`flex items-center gap-1 text-sm text-error-red ${content && 'mt-2'}`}>
                  Error generating the response
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatMessages;