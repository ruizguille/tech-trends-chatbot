import Markdown from 'react-markdown';
import useAutoScroll from '@/hooks/useAutoScroll';
import Spinner from '@/components/Spinner';
import userIcon from '@/assets/images/user.svg';
import botIcon from '@/assets/images/bot.svg';
import errorIcon from '@/assets/images/error.svg';

function ChatMessages({ messages, isLoading, typingText, isTyping }) {
  const scrollContentRef = useAutoScroll(isLoading || isTyping);

  return (
      <div ref={scrollContentRef} className="grow space-y-4">
        {messages.map(({ role, content, loading, error }, idx) => (
            <div
                key={idx}
                className={`flex items-start gap-4 py-4 px-4 rounded-xl transition-colors duration-300 ${
                    role === 'user'
                        ? 'bg-gray-700 text-white'
                        : 'bg-gray-800 text-gray-100'
                }`}
            >
              {role === 'user' ? (
                  <img
                      className="h-8 w-8 shrink-0 rounded-full bg-blue-500 p-1"
                      src={userIcon}
                      alt="user"
                  />
              ) : (
                  <img
                      className="h-8 w-8 shrink-0 rounded-full bg-orange-500 p-1"
                      src={botIcon}
                      alt="assistant"
                  />
              )}
              <div className="flex-1">
                <div className="markdown-container">
                  {(loading && !content) ? (
                      <Spinner />
                  ) : (role === 'assistant') ? (
                      isTyping && idx === messages.length - 1 ? (
                          <Markdown>{typingText}<span className="cursor-blink">|</span></Markdown>
                      ) : (
                          <Markdown>{content}</Markdown>
                      )
                  ) : (
                      <div className="whitespace-pre-line">{content}</div>
                  )}
                </div>
                {error && (
                    <div className={`flex items-center gap-1 text-sm text-red-400 ${content && 'mt-2'}`}>
                      <img className="h-5 w-5" src={errorIcon} alt="error" />
                      <span>Error generating the response</span>
                    </div>
                )}
              </div>
            </div>
        ))}
      </div>
  );
}

export default ChatMessages;