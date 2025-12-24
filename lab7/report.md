# Лабораторная работа №7
# АСИНХРОННОЕ ПРОГРАММИРОВАНИЕ В GO

**Дата:** 2025-12-24  

**Семестр:** 2 курс, 1 полугодие (3 семестр)  

**Группа:** ПИН-б-о-24-1  

**Дисциплина:** Технологии программирования  

**Студент:** Куйбышев Александр Максимович  

## Цель работы

Изучение механизмов асинхронного и конкурентного программирования в языке Go. В ходе работы необходимо освоить использование горутин, каналов и основных паттернов параллелизма, а также реализовать и протестировать примеры асинхронных программ.


### Среда выполнения

Работа выполнена в операционной системе **macOS** с использованием терминала и компилятора Go.


### Выполненные задачи

* Создание и использование горутин
* Синхронизация с помощью WaitGroup
* Передача данных через каналы
* Реализация паттерна Worker Pool
* Pеализация Pipeline
* Реализация Fan-Out / Fan-In

### Структура проекта

```
lab-07/project
├── main.go
├── channels.go
├── goroutines.go
└── worker_pool.go
```


## Реализация и примеры кода

### Пример 1. Базовая горутина

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Горутина %d работает\n", id)
        }(i)
    }

    wg.Wait()
    fmt.Println("Все горутины завершены")
}
```

**Описание:**
В данном примере создаются три горутины, которые выполняются параллельно. WaitGroup используется для ожидания их завершения.


### Пример 2. Каналы (Producer–Consumer)

```go
package main

import "fmt"

func main() {
    ch := make(chan int)

    go func() {
        for i := 1; i <= 5; i++ {
            ch <- i
        }
        close(ch)
    }()

    for val := range ch {
        fmt.Println("Получено:", val)
    }
}
```

**Описание:**
Одна горутина отправляет данные в канал, другая — принимает их.

### Пример 3. Worker Pool

```go
package main

import (
    "fmt"
    "sync"
)

func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    for job := range jobs {
        results <- job * job
    }
}

func main() {
    jobs := make(chan int, 5)
    results := make(chan int, 5)

    var wg sync.WaitGroup

    for w := 1; w <= 3; w++ {
        wg.Add(1)
        go worker(w, jobs, results, &wg)
    }

    for i := 1; i <= 5; i++ {
        jobs <- i
    }
    close(jobs)

    wg.Wait()
    close(results)

    for res := range results {
        fmt.Println("Результат:", res)
    }
}
```

### Пример 4. Pipeline

```go
package main

import "fmt"

func stage1(nums []int) []int {
    out := []int{}
    for _, n := range nums {
        out = append(out, n*2)
    }
    return out
}

func stage2(nums []int) []int {
    out := []int{}
    for _, n := range nums {
        out = append(out, n+1)
    }
    return out
}

func main() {
    input := []int{1, 2, 3, 4, 5}
    result := stage2(stage1(input))
    fmt.Println(result)
}
```

### Пример 5. Fan-Out / Fan-In

```go
package main

import "fmt"

func square(ch <-chan int, out chan<- int) {
    for n := range ch {
        out <- n * n
    }
}

func main() {
    input := make(chan int)
    output := make(chan int)

    for i := 0; i < 3; i++ {
        go square(input, output)
    }

    go func() {
        for i := 1; i <= 5; i++ {
            input <- i
        }
        close(input)
    }()

    for i := 1; i <= 5; i++ {
        fmt.Println(<-output)
    }
}
```

## Результаты выполнения

Программа корректно выполняет параллельные вычисления, демонстрируя работу горутин, каналов и паттернов параллелизма. Ошибок синхронизации и race conditions выявлено не было.

## Выводы

- В ходе выполнения лабораторной работы были изучены основные механизмы асинхронного программирования в Go. Горутины позволяют легко создавать параллельные задачи, а каналы обеспечивают безопасный обмен данными между ними.

- Использование паттернов параллелизма (Worker Pool, Pipeline, Fan-Out/Fan-In) упрощает разработку масштабируемых и производительных приложений. Язык Go предоставляет удобные и понятные средства для реализации конкурентных программ, что делает его подходящим для серверных и высоконагруженных систем.
