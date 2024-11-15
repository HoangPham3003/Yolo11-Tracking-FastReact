import React from 'react';
import './App.scss';


interface AppState {
    image_base64: string;
    fps: number;
    laneCounts: {
        lane1: number;
        lane2: number;
        lane3: number;
    };
    connectionStatus: string;  // New state for connection status
    showRefreshPrompt: boolean; // New state for showing the refresh prompt
}


class App extends React.Component<{}, AppState> {

    private eventSource: EventSource | undefined;
    private frameCount: number = 0

    constructor(props: {}) {
        super(props);
        this.state = {
            image_base64: '',
            fps: 0,
            laneCounts: {
                lane1: 0,
                lane2: 0,
                lane3: 0
            },
            connectionStatus: 'Connected',  // Initial connection status
            showRefreshPrompt: false  // Initially hide the refresh prompt
        };
    }

    componentDidMount() {

        const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // Default to localhost if not set
        this.eventSource = new EventSource(`${apiUrl}/`);
        this.setState({
            connectionStatus: 'Connected',
            showRefreshPrompt: false
        });

        this.eventSource.onmessage = (event: MessageEvent) => {
            this.frameCount += 1;
            const data = JSON.parse(event.data);
            if (this.frameCount % 1 === 0) {
                this.setState({
                    image_base64: data.frame_base64,
                    fps: data.fps,
                    laneCounts: data.lane_counts,
                    connectionStatus: 'Connected'
                });
            }
        };

        this.eventSource.onerror = (error) => {
            console.error("Error in SSE connection:", error);
            this.setState({
                connectionStatus: 'Disconnected',
                showRefreshPrompt: true
            });
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = undefined;
            }
        };
    }

    componentWillUnmount() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = undefined;
        }
    }


    // Function to render the refresh prompt modal
    renderRefreshPrompt = () => {
        return (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
                <div className="bg-white p-6 rounded-lg shadow-lg text-center max-w-sm">
                    <h2 className="text-2xl font-bold mb-4 text-red-600">Connection Issue</h2>
                    <p className="text-gray-700 mb-4">It looks like the connection was lost. Please refresh the page to try reconnecting.</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="bg-blue-600 text-white py-2 px-4 rounded-md"
                    >
                        Refresh Page
                    </button>
                </div>
            </div>
        );
    };

    render() {
        const { image_base64, fps, laneCounts, connectionStatus, showRefreshPrompt } = this.state;
        return (
            <div className="flex flex-col items-center p-6 space-y-6 bg-gray-100 min-h-screen">
                <h1 className="text-3xl font-bold text-red-600">Streaming: Cars Tracking</h1>

                <div className="w-full max-w-3xl bg-white shadow-lg rounded-lg p-4 flex flex-col items-center space-y-4">
                    <img
                        src={`data:image/jpeg;base64,${image_base64}`}
                        className="w-full rounded-md"
                    />

                    <div className="text-center">
                        <p className="text-lg font-semibold">
                            <span className="text-gray-600">FPS:</span> {fps.toFixed(2)}
                        </p>
                    </div>

                    <div className="grid grid-cols-3 gap-4 w-full text-center">
                        <div className="bg-blue-100 rounded-lg p-4">
                            <p className="text-gray-700 font-medium">Lane 1</p>
                            <p className="text-2xl font-bold text-blue-600">{laneCounts.lane1}</p>
                        </div>
                        <div className="bg-green-100 rounded-lg p-4">
                            <p className="text-gray-700 font-medium">Lane 2</p>
                            <p className="text-2xl font-bold text-green-600">{laneCounts.lane2}</p>
                        </div>
                        <div className="bg-yellow-100 rounded-lg p-4">
                            <p className="text-gray-700 font-medium">Lane 3</p>
                            <p className="text-2xl font-bold text-yellow-600">{laneCounts.lane3}</p>
                        </div>
                    </div>
                </div>
                {showRefreshPrompt && this.renderRefreshPrompt()}
            </div>
        );
    }
}

export default App;
