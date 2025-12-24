package main

import (
	"context"
	"fmt"
	"lab-async-go/internal/async"
	"lab-async-go/internal/server"
	"strings"
	"sync"
	"time"
)

func main() {
	fmt.Println("Асинхронное программирование")
	fmt.Println(strings.Repeat("=", 60))

	fmt.Println("\n1. Базовые горутины")
	example1BasicGoroutine()

	fmt.Println("\n2. Counter")
	example2Counter()

	fmt.Println("\n3. MapConcurrent")
	example3MapConcurrent()

	fmt.Println("\n4. FilterConcurrent")
	example4FilterConcurrent()

	fmt.Println("\n5. ReduceConcurrent")
	example5ReduceConcurrent()

	fmt.Println("\n6. Producer-Consumer pattern")
	example6ProducerConsumer()

	fmt.Println("\n7. Pipeline")
	example7Pipeline()

	fmt.Println("\n8. Fan-Out/Fan-In")
	example8FanOutFanIn()

	fmt.Println("\n9. Worker Pool")
	example9WorkerPool()

	fmt.Println("\n10. HTTP Server")
	example10HTTPServer()
}

func example1BasicGoroutine() {
	var wg sync.WaitGroup
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf("  Горутина %d: processing\n", id)
			time.Sleep(100 * time.Millisecond)
			fmt.Printf("  Горутина %d: done\n", id)
		}(i)
	}
}

func example2Counter() {
	counter := async.NewCounter()
	var wg sync.WaitGroup

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				counter.Increment()
			}
		}()
	}

	wg.Wait()
	fmt.Printf("Counter = %d\n", counter.Value())
}

func example3MapConcurrent() {
	data := []int{1, 2, 3, 4, 5}
	result := async.MapConcurrent(data, func(x int) int {
		return x * x
	})
	fmt.Printf("start: %v\n", data)
	fmt.Printf("result (x^2): %v\n", result)
}

func example4FilterConcurrent() {
	data := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	result := async.FilterConcurrent(data, func(x int) bool {
		return x%2 == 0
	})
	fmt.Printf("start: %v\n", data)
	fmt.Printf("result: %v\n", result)
}

func example5ReduceConcurrent() {
	data := []int{1, 2, 3, 4, 5}
	sum := async.ReduceConcurrent(data, 0, func(acc, x int) int {
		return acc + x
	})
	fmt.Printf("Массив: %v\n", data)
	fmt.Printf("sum: %d\n", sum)
}

func example6ProducerConsumer() {
	ch := make(chan int, 10)
	go async.Producer(ch, 5)
	async.Consumer(ch, 5)
	fmt.Println("Обмен данных done")
}

func example7Pipeline() {
	ctx := context.Background()
	input := []int{1, 2, 3, 4, 5}

	output := async.Pipeline(ctx, input,
		func(x int) int { return x * 2 },
		func(x int) int { return x + 10 },
	)

	fmt.Printf("start: %v\n", input)
	fmt.Printf("done: %v\n", output)
}

func example8FanOutFanIn() {
	ctx := context.Background()
	input := []int{1, 2, 3, 4, 5}

	channels := async.FanOut(ctx, input, 3)
	result := async.FanIn(ctx, channels...)

	fmt.Printf("start: %v\n", input)
	fmt.Printf("done: %v\n", result)
}

func example9WorkerPool() {
	pool := async.NewWorkerPool(3)
	tasks := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	results := pool.ProcessTasks(tasks, func(task int) string {
		return fmt.Sprintf("результат-%d", task*task)
	})

	fmt.Printf("tasks: %d\n", len(tasks))
	fmt.Printf("results: %d\n", len(results))
	fmt.Printf("examples: %v\n", results[:3])
}

func example10HTTPServer() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	srv := server.NewServer(":8080")
	go srv.Start()
	defer srv.Stop(ctx)

	fmt.Println("Сервер запущен на :8080")
	fmt.Println("Graceful shutdown включен")
	time.Sleep(2 * time.Second)
}
