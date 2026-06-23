# async-web-crawler-indexer
A high-performance concurrent web crawler and inverted search index built in Python using Asyncio

# 🕷️ Google-Caliber Asynchronous Web Crawler & Inverted Search Indexer

A high-performance, concurrent web discovery and text indexing engine built from scratch in Python. This system demonstrates advanced asynchronous I/O architectures, dynamic graph-traversal link discovery (BFS), data structure optimizations, and local database persistence layers without relying on heavy external scraping frameworks.

---

## 🚀 **Architectural Overview**

Modern search engines rely on highly efficient, concurrent workflows to map the web. This project splits that challenge into two primary software engineering subsystems: an **Asynchronous Page Fetching Pipeline** and an **Inverted Search Indexing Core**.

1. **The Async Crawler:** Utilizing `asyncio` and `httpx`, the engine fires non-blocking I/O requests across target network endpoints simultaneously, achieving maximum network throughput.
2. **The Inverted Index Engine:** Rather than wasting compute searching documents sequentially, raw HTML text is cleaned, tokenized, and mapped backwards—pairing unique keywords directly to arrays of source URLs for fast $O(1)$ dictionary lookups.

---

## 🛠️ **Deep-Dive Core Engineering Features**

* **Concurrent Network I/O Stream:** Engineered utilizing Python’s `asyncio` loop topology combined with `httpx.AsyncClient`. This avoids thread-blocking traps, permitting hundreds of concurrent socket operations over a lightweight single-thread engine.
* **Dynamic Graph Link Discovery (BFS):** Implements a robust Breadth-First Search (BFS) traversal algorithm. As HTML streams parse, the system instantly strips out anchors (`<a>` tags), validates domain constraints, and feeds them back into a dynamic execution queue to automatically crawl deeper into the site.
* **Custom Async Resource Lifecycle Manager:** Utilizes Python’s asynchronous context manager magic methods (`__aenter__` and `__aexit__`) to guarantee deterministic connection pool creation and strict cleanup closures, wiping out potential socket and execution leaks.
* **Relational Intersecting Search Engine:** Supports multi-word keyword evaluation by running mathematical intersection set logic across index keys. A search query for `"tutorial code"` isolates only the exact web pages matching *all* terms simultaneously.
* **Static Database Persistence Layer:** Intercepts system closing events to securely dump runtime memory maps out into structured, human-readable local JSON files (`index.json`).

---

## 📁 Repository File Layout

```text
📦 async-web-crawler-indexer
 ┣ 📜 crawler.py          # Asynchronous crawler execution logic & UI engine
 ┣ 📜 index.json          # Persistent local Inverted Index database output
 ┗ 📜 requirements.txt    # Production


🏃Getting Started & Local Installation
Prerequisites

Make sure you have Python 3.8+ installed on your operating system.
1. Clone the Repository

2. Install Project Dependencies
Decouple your local machine environment and pull the exact stable packages required using pip:

pip install -r requirements.txt

3. Execute the System Engine
Run the core pipeline script to watch the crawler auto-discover pages and spin up the interactive terminal engine:

python crawler.py

🎯 Verification & Sample Run

Terminal Execution Trace:

--- Running Production Asynchronous Discovery Crawler ---
🕷️ [1/8] Crawling: [https://docs.python.org/3/tutorial/index.html](https://docs.python.org/3/tutorial/index.html)
🕷️ [2/8] Crawling: [https://docs.python.org/3/tutorial/appended.html](https://docs.python.org/3/tutorial/appended.html)
💾 Database saved successfully to 'index.json'!

==================================================
🔍 RELATIONAL INTERSECTING SEARCH ENGINE READY
==================================================


Enter search keywords (or type 'exit'): tutorial functions
🎯 Found 2 page(s) for 'tutorial functions':
  1. [https://docs.python.org/3/tutorial/index.html](https://docs.python.org/3/tutorial/index.html)
  2. [https://docs.python.org/3/library/functions.html](https://docs.python.org/3/library/functions.html)


Generated Inverted Index Database Blueprint (index.json snippet):

{
    "tutorial": [
        "[https://docs.python.org/3/tutorial/index.html](https://docs.python.org/3/tutorial/index.html)",
        "[https://docs.python.org/3/tutorial/introduction.html](https://docs.python.org/3/tutorial/introduction.html)"
    ],
    "asynchronous": [
        "[https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)"
    ]
}


💡 System Design Key Takeaways

Network Fault Tolerance: The pipeline embeds custom try/except blocks around I/O pools to catch bad nodes or unexpected HTTP statuses (like 404 or 500 errors) gracefully without destabilizing the remaining execution stack.

Polite Crawling Latency Caps: Includes automated asyncio.sleep routines between fetch operations to maintain polite rate limits against external server hosts.

Data Denormalization: Trade runtime storage memory space to optimize lookup velocity, reducing complex multi-document text scans down to direct key hash evaluations.
