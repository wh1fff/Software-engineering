package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"sync"
	"sync/atomic"
	"time"
)

type Server struct {
	addr        string
	httpServer  *http.Server
	requestsCh  chan int
	stopChan    chan struct{}
	requestMu   sync.Mutex
	requestsNum int64
}

func NewServer(addr string) *Server {
	srv := &Server{
		addr:       addr,
		requestsCh: make(chan int, 100),
		stopChan:   make(chan struct{}),
	}

	mux := http.NewServeMux()
	srv.setupRoutes(mux)

	srv.httpServer = &http.Server{
		Addr:    addr,
		Handler: srv.middleware(mux),
	}

	return srv
}

func (s *Server) setupRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/", s.handleRoot)
	mux.HandleFunc("/health", s.handleHealth)
	mux.HandleFunc("/stats", s.handleStats)
	mux.HandleFunc("/echo", s.handleEcho)
	mux.HandleFunc("/delay", s.handleDelay)
	mux.HandleFunc("/heavy", s.handleHeavy)
}

func (s *Server) middleware(next http.Handler) http.Handler {
	return s.loggingMiddleware(s.recoveryMiddleware(next))
}

func (s *Server) loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		atomic.AddInt64(&s.requestsNum, 1)

		next.ServeHTTP(w, r)

		duration := time.Since(start)
		log.Printf("%s %s %s %v", r.Method, r.RequestURI, r.RemoteAddr, duration)
	})
}

func (s *Server) recoveryMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("Panic: %v", err)
				w.WriteHeader(http.StatusInternalServerError)
				fmt.Fprintf(w, "Internal Server Error")
			}
		}()
		next.ServeHTTP(w, r)
	})
}

func (s *Server) handleRoot(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprintf(w, "Lab Async Go - HTTP Server\n")
	fmt.Fprintf(w, "Попробуйте: /health, /stats, /echo?message=text\n")
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"status":"ok"}`)
}

func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	requests := atomic.LoadInt64(&s.requestsNum)
	fmt.Fprintf(w, `{"requests":%d}`, requests)
}

func (s *Server) handleEcho(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	message := r.URL.Query().Get("message")
	fmt.Fprintf(w, `{"echo":"%s"}`, message)
}

func (s *Server) handleDelay(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	secondsStr := r.URL.Query().Get("seconds")
	seconds := 0.1
	fmt.Sscanf(secondsStr, "%f", &seconds)

	time.Sleep(time.Duration(seconds*1000) * time.Millisecond)

	fmt.Fprintf(w, `{"delayed":true}`)
}

func (s *Server) handleHeavy(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	sum := 0
	for i := 0; i < 1000000; i++ {
		sum += i
	}

	fmt.Fprintf(w, `{"result":%d}`, sum)
}

// Start
func (s *Server) Start() {
	log.Printf("Сервер запущен на %s", s.addr)
	if err := s.httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Printf("Ошибка сервера: %v", err)
	}
}

// Stop
func (s *Server) Stop(ctx context.Context) {
	if err := s.httpServer.Shutdown(ctx); err != nil {
		log.Printf("Ошибка shutdown: %v", err)
	}
	log.Println("Сервер остановлен")
}
