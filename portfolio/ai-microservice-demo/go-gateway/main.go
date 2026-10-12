package main

import (
    "encoding/json"
    "io"
    "log"
    "net/http"
    "os"
    "time"
)

func main() {
    mlBaseURL := os.Getenv("ML_SERVICE_URL")
    if mlBaseURL == "" {
        mlBaseURL = "http://api:8000"
    }

    client := &http.Client{Timeout: 3 * time.Second}

    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        _ = json.NewEncoder(w).Encode(map[string]string{"status": "ok", "service": "go-gateway"})
    })

    http.HandleFunc("/ml-health", func(w http.ResponseWriter, r *http.Request) {
        resp, err := client.Get(mlBaseURL + "/health")
        if err != nil {
            http.Error(w, `{"status":"unavailable"}`, http.StatusBadGateway)
            return
        }
        defer resp.Body.Close()
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(resp.StatusCode)
        _, _ = io.Copy(w, resp.Body)
    })

    log.Println("Go gateway listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
