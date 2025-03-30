import Chatbot from '@/components/Chatbot';
import logo from '@/assets/images/logo.svg';

function App() {
    return (
        <div className="flex flex-col min-h-full w-full max-w-3xl mx-auto px-4 bg-gray-900 text-gray-100">
            <header className="sticky top-0 shrink-0 z-20 bg-gray-900 border-b border-gray-800">
                <div className="flex flex-col h-full w-full gap-1 pt-4 pb-2">
                    <a href="https://codeawake.com" className="inline-block">
                        <img src={logo} className="w-32 invert" alt="logo" />
                    </a>
                    <h1 className="font-urbanist text-[1.65rem] font-semibold text-blue-400">
                        Tech Trends AI Chatbot
                    </h1>
                </div>
            </header>
            <Chatbot />
        </div>
    );
}

export default App;