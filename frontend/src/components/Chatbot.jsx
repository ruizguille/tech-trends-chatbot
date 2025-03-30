import { useState, useEffect, useRef } from 'react';
import { useImmer } from 'use-immer';
import api from '@/api';
import { parseSSEStream } from '@/utils';
import ChatMessages from '@/components/ChatMessages';
import ChatInput from '@/components/ChatInput';
import FileUpload from '@/components/FileUpload';

function Chatbot() {
  const [chatId, setChatId] = useState(null);
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState('');
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [typingText, setTypingText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const fullResponseRef = useRef('');

  const isLoading = messages.length && messages[messages.length - 1].loading;

  // Typing effect implementation
  useEffect(() => {
    if (isTyping && fullResponseRef.current) {
      const textToType = fullResponseRef.current;
      let index = 0;

      const typingInterval = setInterval(() => {
        if (index < textToType.length) {
          setTypingText(textToType.substring(0, index + 1));
          index++;
        } else {
          clearInterval(typingInterval);
          setIsTyping(false);

          // Update the actual message content when typing is complete
          setMessages(draft => {
            const lastMessage = draft[draft.length - 1];
            if (lastMessage.role === 'assistant') {
              lastMessage.content = textToType;
              lastMessage.loading = false;
            }
          });
        }
      }, 20); // Adjust speed of typing here

      return () => clearInterval(typingInterval);
    }
  }, [isTyping, setMessages]);

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages(draft => [...draft,
      { role: 'user', content: trimmedMessage },
      { role: 'assistant', content: '', sources: [], loading: true }
    ]);
    setNewMessage('');
    setShowFileUpload(false);

    let chatIdOrNew = chatId;
    try {
      if (!chatId) {
        const { id } = await api.createChat();
        setChatId(id);
        chatIdOrNew = id;
      }

      fullResponseRef.current = ''; // Reset the full response

      const stream = await api.sendChatMessage(chatIdOrNew, trimmedMessage);
      for await (const textChunk of parseSSEStream(stream)) {
        fullResponseRef.current += textChunk;

        // Start typing effect when we get the first chunk
        if (!isTyping) {
          setIsTyping(true);
        }
      }

      // If typing effect is not active, update message directly
      if (!isTyping) {
        setMessages(draft => {
          draft[draft.length - 1].content = fullResponseRef.current;
          draft[draft.length - 1].loading = false;
        });
      }
    } catch (err) {
      console.error(err);
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
      setIsTyping(false);
    }
  }

  function handleFileUpload(files) {
    // This would be implemented when you add RAG/multimodal capabilities
    console.log('Files selected:', files);

    // Here you would normally upload the files to your backend
    // For now, we'll just create a message showing what was uploaded
    if (files && files.length > 0) {
      const fileNames = Array.from(files).map(file => file.name).join(', ');
      setMessages(draft => [...draft,
        { role: 'user', content: `Uploaded files: ${fileNames}` }
      ]);
    }

    setShowFileUpload(false);
  }

  return (
      <div className="relative grow flex flex-col gap-6 pt-6">
        {messages.length === 0 && (
            <div className="mt-3 font-urbanist text-gray-300 text-xl font-light space-y-2">
              <p>👋 Welcome!</p>
              <p>I am powered by the latest technology reports from leading institutions like the World Bank, the World Economic Forum, McKinsey, Deloitte and the OECD.</p>
              <p>Ask me anything about the latest technology trends.</p>
            </div>
        )}
        <ChatMessages
            messages={messages}
            isLoading={isLoading}
            typingText={typingText}
            isTyping={isTyping}
        />
        {showFileUpload && (
            <FileUpload onUpload={handleFileUpload} onCancel={() => setShowFileUpload(false)} />
        )}
        <ChatInput
            newMessage={newMessage}
            isLoading={isLoading}
            setNewMessage={setNewMessage}
            submitNewMessage={submitNewMessage}
            toggleFileUpload={() => setShowFileUpload(!showFileUpload)}
        />
      </div>
  );
}

export default Chatbot;