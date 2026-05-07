# Stress Testing

Stress testing evaluates how the LLM performs under load, measuring response times, throughput, and quality across different scenarios. This section demonstrates stress testing with the **Gemma 4 E4B** model.

## Test Workflow

```mermaid
flowchart TD
    A[Test Cases] --> B[Test Runner]
    B --> C[Sequential Mode]
    B --> D[Parallel Mode]
    C --> E[Measure Latency]
    D --> E
    E --> F[Collect Results]
    F --> G[Generate Report]
    
    style A fill:#e3f2fd
    style G fill:#c8e6c9
```

## Test Execution Flow

```mermaid
flowchart LR
    subgraph Setup
        A[Load Test Cases] --> B[Configure Runner]
    end
    
    subgraph Execution
        B --> C[Call LLM API]
        C --> D{Success?}
        D -->|Yes| E[Record Response]
        D -->|No| F[Log Error]
        E --> G{Next Case?}
        F --> G
        G -->|Yes| C
        G -->|No| H[Complete]
    end
    
    subgraph Results
        H --> I[Calculate Stats]
        I --> J[Generate Report]
    end
    
    style J fill:#c8e6c9
```

## Performance Metrics

```mermaid
graph TD
    A[Stress Test Results] --> B[Response Time]
    A --> C[Throughput]
    A --> D[Error Rate]
    A --> E[Quality Score]
    
    B --> F[Min/Avg/Max]
    C --> G[Requests/sec]
    D --> H[Success vs Fail]
    E --> I[Accuracy Check]
    
    style F fill:#e8eaf6
    style G fill:#e8eaf6
    style H fill:#e8eaf6
    style I fill:#e8eaf6
```

## Test Case Structure

| Test Type | Cases | Purpose |
|-----------|-------|---------|
| Mini Demo | 5 | Quick validation |
| Small Demo | 10 | Basic functionality |
| Standard Test | 55 | Comprehensive evaluation |
| Stress Test | 100+ | Performance limits |

## Sequential vs Parallel

```mermaid
flowchart LR
    subgraph Sequential
        A[T1] --> B[T2] --> C[T3] --> D[T4]
        style A fill:#e3f2fd
        style D fill:#c8e6c9
    end
    
    subgraph Parallel
        E[T1] --> H[All at Once]
        F[T2] --> H
        G[T3] --> H
        G[T4] --> H
        style E fill:#e3f2fd
        style H fill:#c8e6c9
    end
```

## Test Reports

```mermaid
sequenceDiagram
    participant T as Test Runner
    participant L as LLM API
    participant R as Report Generator
    
    loop For each case
        T->>L: Send request
        L-->>T: Response + time
        T->>T: Record metrics
    end
    
    T->>R: Generate report
    R-->>T: Report complete
```

## Demo Scripts

| Script | Cases | Description |
|--------|-------|-------------|
| `llm_mini_demo_5cases.py` | 5 | Quick sanity check |
| `llm_demo_small_10case.py` | 10 | Standard validation |
| `llm_hierarchical_demo.py` | 15 | Multi-level testing |
| `gemma-4-e4b-llm_stress_test_class.py` | 55+ | Full stress test |

## Running Tests

```bash
# Quick validation (5 cases)
python llm_mini_demo_5cases.py

# Standard test (10 cases)
python llm_demo_small_10case.py

# Full stress test (55+ cases)
python gemma-4-e4b-llm_stress_test_class.py
```

## Expected Output

```
Test Run: 55 cases
Mode: Sequential
Model: Gemma 4 E4B

Results:
- Total Time: 45.2s
- Avg Response: 0.82s
- Min/Max: 0.3s / 2.1s
- Errors: 0
- Success Rate: 100%

Quality Metrics:
- Classification Accuracy: 91%
- Reasoning Correctness: 88%
```

## Performance Thresholds

| Metric | Target | Critical |
|--------|--------|----------|
| Avg Response Time | <1s | >2s |
| Max Response Time | <3s | >5s |
| Error Rate | <1% | >5% |
| Throughput | >10 req/s | <5 req/s |

## Test Configuration

```mermaid
graph TD
    A[Test Config] --> B[Model Settings]
    A --> C[API Endpoint]
    A --> D[Test Cases]
    A --> E[Thresholds]
    
    B --> F[Temp, Top-P, Max Tokens]
    C --> G[Port, Timeout]
    D --> H[Cases JSON]
    E --> I[Pass/Fail Criteria]
    
    style I fill:#c8e6c9
```

## Interpreting Results

- **Low avg time, high max time**: Occasional slow responses (normal)
- **High error rate**: Check API connectivity and model health
- **Quality drops under load**: Consider model upgrade or optimization

*Stress testing ensures your LLM deployment can handle expected workloads reliably.*

## Best Practices

1. Run tests during off-peak hours
2. Use representative test cases
3. Monitor system resources (CPU, RAM)
4. Compare results across model versions
5. Document and track performance over time

## Automation

Schedule regular stress tests to ensure consistent performance:

```bash
# Add to cron/scheduler
0 */6 * * * python llm_stress_test_class.py >> /var/log/llm-stress.log
```

This helps catch performance degradation before it impacts users.