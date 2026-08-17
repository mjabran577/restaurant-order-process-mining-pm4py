# Process Mining Analysis of a Restaurant Order Fulfillment Process

**Business Analytics – Group Project Executive Summary**

**Authors:** Muhammad Jabran and Nusrat Jahan Iba  
**University of Bayreuth – Faculty of Life Sciences: Food, Nutrition and Health, Campus Kulmbach**

## 1. Introduction and data overview

The project analyzes an event log describing a restaurant kitchen order-fulfillment process. The complete dataset contains **45,379 events across 7,549 individual orders** over several years. Each order is represented as a sequence of timestamped activities, beginning with the order being placed and ending either with the order being served or rejected.

Following the assignment rule, the dataset was filtered to the year **2030**. This produced **68 orders and 371 events**. To focus on the normal successful fulfillment process, orders ending in rejection were removed, leaving **44 completed orders and 299 events**.

The process includes order arrival, ingredient checking, food preparation, oven preheating, cooking, spicing, and serving. Eight staff resources appear in the full event log.

## 2. Process model

PM4Py's inductive miner was used to discover both a **Petri net** and a **BPMN model**. With rejected cases removed, the discovered process is mostly linear and therefore comparatively easy to interpret.

The corresponding visual models are available in the repository's `figures/` directory.

## 3. Process map and bottleneck identification

A frequency directly-follows graph (DFG) was used to show how often activities transition into one another, while a performance DFG was used to examine the average time between activities.

The clearest direct bottleneck is the transition from **Food prepared → Food cooked**, with a mean duration of **143.4 hours** and a standard deviation of **69.4 hours**.

| Process step | Mean duration | Std. deviation |
|---|---:|---:|
| Food prepared → Food cooked | 143.4 h | 69.4 h |
| Ingredients checked → Food spiced* | 142.5 h | 61.0 h |
| Food spiced → Order served | 112.3 h | 67.8 h |
| Order arrives → Ingredients checked | 42.3 h | 23.6 h |
| Oven preheated → Food cooked | 34.5 h | 27.1 h |

\*This pair skips an intermediate step in some traces and is included for completeness. The preparation-to-cooking transition is the more reliable direct bottleneck indicator.

The preparation-to-cooking stage is notable not only because it is slow, but because it is highly variable. That makes the process less predictable. By comparison, the transition from order arrival to ingredient checking is faster and more consistent.

## 4. Business interpretation

If the event log represented a real operating process, management attention should first focus on the preparation-to-cooking stage. Possible causes could include staff scheduling, capacity constraints, or oven availability, although the event log itself can identify **where** a delay occurs rather than prove **why** it occurs.

The mean end-to-end time from order arrival to service is **296.8 hours** in the filtered dataset. Reducing both the duration and variability of the identified bottleneck would improve overall process predictability.

## 5. Broader application of process mining

The same approach can be applied to operational event data in many settings. Hospitals can use process mining to identify delays between admission and discharge; manufacturers can analyze production and quality-check bottlenecks; and banks or insurers can examine where applications or claims become delayed.

The common idea is to reconstruct the **actual process from timestamped data**, rather than relying only on how the process is expected to work on paper.

## 6. Limitations

The filtered analysis contains only **44 completed orders from a single year**, which is small compared with the full event log. A real production analysis would need a larger evidence base and direct engagement with operational staff before drawing firm conclusions about causes.

A more fundamental limitation is that the event log is **simulated**. Multi-day gaps between restaurant activities are not realistic for an actual kitchen. The numerical timings should therefore be interpreted as an illustration of the process-mining methodology, not as a real-world restaurant benchmark.

## 7. Conclusion

The analysis demonstrates how even a simple process can contain a substantial and inconsistent bottleneck when actual timestamps are analyzed. The **Food prepared → Food cooked** transition is the strongest direct candidate for operational improvement in the filtered process.

More broadly, the project demonstrates how process mining can convert operational event data into reproducible process models, timing evidence, bottleneck identification, and management-oriented recommendations.
