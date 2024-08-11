import useAutoScroll from '@/hooks/useAutoScroll';
import Spinner from '@/components/Spinner';
import assistantIcon from '@/assets/images/assistant.svg';
import userIcon from '@/assets/images/user.svg';

function ChatMessages({ messages, isLoading }) {
  const scrollContentRef = useAutoScroll(isLoading);
  
  return (
    <div ref={scrollContentRef} className='grow space-y-4'>
      {messages.length === 0 && (
        <div className='mt-3 px-3 text-primary-blue text-lg'>Ask questions about the knowledge base</div>
      )}
      {messages.map(({ role, content, loading, error }, idx) => (
        <div key={idx} className={`flex items-start gap-4 py-4 px-3 rounded-xl ${role === 'user' ? 'bg-primary-blue/10' : ''}`}>
          {role === 'user' && (
            <img
              className='h-[26px] w-[26px] shrink-0'
              src={role === 'user' ? userIcon : assistantIcon}
              alt='user'
            />
          )}
          <div>
            <div className='markdown-container'>
              {(loading && !content) ? <Spinner />
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
  );
}

export default ChatMessages;