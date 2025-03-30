import { useRef, useState } from 'react';
import closeIcon from '@/assets/images/close.svg';

function FileUpload({ onUpload, onCancel }) {
    const [dragActive, setDragActive] = useState(false);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const inputRef = useRef(null);

    function handleDrag(e) {
        e.preventDefault();
        e.stopPropagation();

        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    }

    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            setSelectedFiles(Array.from(e.dataTransfer.files));
        }
    }

    function handleChange(e) {
        e.preventDefault();
        if (e.target.files && e.target.files.length > 0) {
            setSelectedFiles(Array.from(e.target.files));
        }
    }

    function handleSubmit() {
        if (selectedFiles.length > 0) {
            onUpload(selectedFiles);
        }
    }

    return (
        <div className="mb-4 bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-gray-200 font-semibold">Upload Files</h3>
                <button
                    onClick={onCancel}
                    className="p-1 hover:bg-gray-700 rounded-full"
                >
                    <img src={closeIcon} alt="close" className="w-5 h-5" />
                </button>
            </div>

            <div
                className={`relative flex flex-col items-center justify-center h-32 border-2 border-dashed rounded-lg transition-colors ${
                    dragActive ? 'border-blue-500 bg-gray-700' : 'border-gray-600'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    ref={inputRef}
                    type="file"
                    multiple
                    onChange={handleChange}
                    className="hidden"
                />

                {selectedFiles.length > 0 ? (
                    <div className="px-4 w-full">
                        <p className="text-gray-300 mb-2">Selected files:</p>
                        <ul className="text-sm text-gray-400 max-h-16 overflow-y-auto">
                            {selectedFiles.map((file, index) => (
                                <li key={index} className="truncate">{file.name}</li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <div className="text-center p-4">
                        <p className="text-gray-300 mb-2">Drag and drop files here, or</p>
                        <button
                            onClick={() => inputRef.current.click()}
                            className="px-4 py-1 bg-blue-600 hover:bg-blue-500 rounded-md text-white text-sm transition-colors"
                        >
                            Browse files
                        </button>
                    </div>
                )}
            </div>

            {selectedFiles.length > 0 && (
                <div className="mt-3 flex justify-end">
                    <button
                        onClick={handleSubmit}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-md text-white text-sm transition-colors"
                    >
                        Upload {selectedFiles.length} {selectedFiles.length === 1 ? 'file' : 'files'}
                    </button>
                </div>
            )}
        </div>
    );
}

export default FileUpload;