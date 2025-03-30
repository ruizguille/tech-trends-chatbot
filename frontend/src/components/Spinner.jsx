function Spinner() {
    return (
        <div className="relative h-12 w-12">
            <span className="spinner-child animate-spinner bg-blue-500" />
            <span className="spinner-child animate-spinner-delayed bg-orange-500" />
        </div>
    );
}

export default Spinner;