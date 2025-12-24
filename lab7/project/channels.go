package async

import (
	"context"
	"sync"
	"time"
)

func Producer(ch chan<- int, count int) {
	for i := 1; i <= count; i++ {
		ch <- i
	}
	close(ch)
}

func Consumer(ch <-chan int, count int) {
	for i := 0; i < count; i++ {
		value := <-ch
		_ = value
	}
}

func MergeChannels(ctx context.Context, channels ...<-chan int) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for _, ch := range channels {
			for value := range ch {
				select {
				case out <- value:
				case <-ctx.Done():
					return
				}
			}
		}
	}()

	return out
}

func FanOut(ctx context.Context, items []int, n int) []<-chan int {
	channels := make([]<-chan int, n)

	for i := 0; i < n; i++ {
		ch := make(chan int)
		channels[i] = ch

		go func(index int, out chan<- int) {
			defer close(out)
			for j := index; j < len(items); j += n {
				select {
				case out <- items[j]:
				case <-ctx.Done():
					return
				}
			}
		}(i, ch)
	}

	return channels
}

func FanIn(ctx context.Context, channels ...<-chan int) []int {
	var results []int
	var wg sync.WaitGroup

	for _, ch := range channels {
		wg.Add(1)
		go func(in <-chan int) {
			defer wg.Done()
			for value := range in {
				select {
				case <-ctx.Done():
					return
				default:
					results = append(results, value)
				}
			}
		}(ch)
	}

	wg.Wait()
	return results
}

func Pipeline(ctx context.Context, input []int, stages ...func(int) int) []int {
	if len(stages) == 0 {
		return input
	}

	result := input
	for _, stage := range stages {
		result = pipelineStage(ctx, result, stage)
	}

	return result
}

func pipelineStage(ctx context.Context, input []int, fn func(int) int) []int {
	var result []int
	var wg sync.WaitGroup

	for _, value := range input {
		wg.Add(1)
		go func(v int) {
			defer wg.Done()
			result = append(result, fn(v))
		}(value)
	}

	wg.Wait()
	return result
}

type RateLimiter struct {
	ticker   *time.Ticker
	ch       chan struct{}
	stopChan chan struct{}
}

func NewRateLimiter(rps int) *RateLimiter {
	rl := &RateLimiter{
		ticker:   time.NewTicker(time.Second / time.Duration(rps)),
		ch:       make(chan struct{}),
		stopChan: make(chan struct{}),
	}

	go func() {
		for {
			select {
			case <-rl.ticker.C:
				select {
				case rl.ch <- struct{}{}:
				case <-rl.stopChan:
					return
				}
			case <-rl.stopChan:
				return
			}
		}
	}()

	return rl
}

func (rl *RateLimiter) Wait() {
	<-rl.ch
}

func (rl *RateLimiter) Stop() {
	rl.ticker.Stop()
	close(rl.stopChan)
}

type Semaphore struct {
	ch chan struct{}
}

func NewSemaphore(limit int) *Semaphore {
	return &Semaphore{
		ch: make(chan struct{}, limit),
	}
}

func (s *Semaphore) Acquire() {
	s.ch <- struct{}{}
}

func (s *Semaphore) Release() {
	<-s.ch
}

type BoundedQueue struct {
	ch chan interface{}
}

func NewBoundedQueue(size int) *BoundedQueue {
	return &BoundedQueue{
		ch: make(chan interface{}, size),
	}
}

func (bq *BoundedQueue) Enqueue(item interface{}) {
	bq.ch <- item
}

func (bq *BoundedQueue) Dequeue() interface{} {
	return <-bq.ch
}
