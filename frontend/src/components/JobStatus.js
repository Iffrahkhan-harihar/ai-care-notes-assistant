// Polls backend job status at intervals and updates UI when processing completes
import { useEffect } from "react";

// Handles background job tracking by repeatedly querying API until completion
function JobStatus({ jobId, setStatus, setResult }) {
  // Starts polling when a new jobId is received
  useEffect(() => {
    let interval;

    // Calls backend to check current job processing state
    const checkStatus = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/job/${jobId}`, {
          method: "GET",
          headers: {
            "x-api-key": "supersecret123"
          }
        });

        const data = await res.json();

        // Stops polling and updates UI once job is completed
        if (data.status === "completed") {
          setStatus("completed");
          setResult(data.result);
          clearInterval(interval);
        }
      } catch (err) {
        console.error("Error polling:", err);
      }
    };

    // Poll every 2 seconds (simple alternative to WebSockets)
    interval = setInterval(checkStatus, 2000); // every 2 sec

    // Cleanup interval to prevent memory leaks when component unmounts
    return () => clearInterval(interval);

  }, [jobId, setStatus, setResult]);

  return null;
}

export default JobStatus;